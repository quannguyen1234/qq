from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import AnonymousUser
from apps.User.models import Doctor,Patient
from apps.PersonalManagement.models import Address
from .models import ConnectDoctor
from .views import receive_order
import json
from channels.db import database_sync_to_async
from apps.User.references import REVERSE_USER_TYPE
from channels.layers import get_channel_layer
import json
from channels_rabbitmq.core import RabbitmqChannelLayer
from channels.db import database_sync_to_async
from .serializers import DoctorAppointmentsSerializer

class AuthenToken:

    async def websocket_connect(self, event):
        await self.accept()
        user=self.scope['user']
        if isinstance(user,AnonymousUser):
            await self.send(json.dumps({
                'data':{
                    "message": "Token is not correct or expired",
                    'status': 401,
                    'flag': False
                }     
            }))
           
            await self.close()
            return False
        return True            
         






class Conversation(AuthenToken,AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.base_user=None
        self.user=None
        self.user_type=None

    async def websocket_connect(self, event):
        check=await super().websocket_connect(event)
        
        if not check:        
            return
        has_permission=False
        self.base_user=self.scope['user']
        self.user_type=await database_sync_to_async(lambda:self.base_user.user_type)()

        if ( await database_sync_to_async(lambda:hasattr(self.base_user,'user_doctor'))()
           and await database_sync_to_async(lambda:hasattr(self.base_user,'user_patient'))() ):
            await self.send(json.dumps({
                'data':{
                    "message": "Forbiden",
                    'status': 404,
                    'flag': False
                }     
            }))
            await self.close()
            return 
            
        elif self.user_type == REVERSE_USER_TYPE['Doctor']:
            self.user= await database_sync_to_async(lambda:self.base_user.user_doctor)()
            # await database_sync_to_async(lambda:ConnectDoctor.objects.filter(doctor=self.user).delete())()

            await create_or_update_conversation(self.user,self.channel_name,'doctor')
            has_permission=True

        elif self.user_type == REVERSE_USER_TYPE['Patient']:
            self.user= await database_sync_to_async(lambda:self.base_user.user_patient)()
            await create_or_update_conversation(self.user,self.channel_name,'patient')
            has_permission=True
        
        if has_permission:
           
            await self.send(json.dumps(
                {
                    'data':{
                        'message':'Access successfully!',
                        'channel':self.channel_name,
                        'status':200,
                        'flag':True
                    }     
                }  
            )) 
        else:
            self.close()

    
    async def websocket_disconnect(self,*agrs,**kwagrs):
        # if isinstance(self.user,AnonymousUser): 
        
        if  self.user_type is not  None:
            if self.user_type==REVERSE_USER_TYPE['Doctor']:
                pass
                # await database_sync_to_async(lambda:ConnectDoctor.objects.filter(doctor=self.user).delete())()
                
                # turn off receving order signal 
                self.user.is_receive=True
                await database_sync_to_async(lambda:self.user.save())()
            

            if self.user_type==REVERSE_USER_TYPE['Patient']:
                pass
                # await database_sync_to_async(lambda:ConnectDoctor.objects.filter(patient=self.user).delete())()
        await self.disconnect(code=None)
                
    async def disconnect(self,code):
        await self.send(json.dumps({
                "data": {
                    "message":"disconnect",
                    "flag":True,
                    "status":200
                },
            }))
        
        await self.close()
            

    async def receive(self, text_data=None, bytes_data=None):

        data=json.loads(text_data)
       
        if data['type']=='doctor-set-address':
          
            await database_sync_to_async(lambda:receive_order(self.base_user,data))()  
            await self.send(json.dumps({
                "data": {
                    "message:":"turn on receiving order doctor signal ",
                    "flag":True,
                    "status":200
                },
            }))
            self.user.is_receive=True
            await database_sync_to_async(lambda:self.user.save())()

        elif data['type']=='patient-choose-doctor':
            
            doctor_id=data['doctor']
            connect=await database_sync_to_async(lambda:ConnectDoctor.objects.get(doctor__doctor_id=doctor_id))()
            await database_sync_to_async(lambda:receive_order(self.base_user,data))()  
            doctor_target_channel=await database_sync_to_async(lambda:connect.doctor_channel)()
          
            # send to doctor interface a message about confirmings
            await self.send_message_to_channel(doctor_target_channel,{
                
                'type':'doctor-confirm-order',
                'message':'Confirming Order!',
                'patient_id':await database_sync_to_async(lambda:self.user.patient_id)(),
                'patient_name':await database_sync_to_async(lambda:self.user.base_user.get_full_name)(),
                "patient_channel":self.channel_name
            })
        elif data['type']=='get-doctors':
            resulf=await get_doctors(data)
            await self.send(json.dumps(resulf))

        elif data['type']=='cancel-order':
            resulf,detail=await cancel_order(data)
            await self.send(json.dumps(resulf))
            await self.send_message_to_channel(detail['doctor_channel'],{
                'message':"patient cancel order",
                'patient_id':detail['patient_id'],
                'flag':True,
                'status':200,
            })

        elif data['type']=='doctor-confirm-order':  
            is_receive_order=data.get('is_receive_order')
            patient_channel=data.get('patient_channel')
            print(data)
            if is_receive_order:
                connect=await database_sync_to_async(lambda:ConnectDoctor.objects.get(doctor=self.user))()
                patient=await database_sync_to_async(Patient.objects.get)(patient_id=data.get('patient_id'))
                connect.patient=patient
                connect.patient_channel=data.get('patient_channel')
                connect.is_confirm=True
                await database_sync_to_async(lambda:connect.save())()
                
                # send the message to client interface
                await self.send_message_to_channel(patient_channel,
                    {
                        'type':'doctor-confirm-order',
                        'flag':True,
                        'status':200,
                        'message':'The doctor has received order',
                        'doctor_id':await database_sync_to_async(lambda:self.user.doctor_id)(),
                        'doctor_name':await database_sync_to_async(lambda:self.user.base_user.get_full_name)()
                    }               
                )    
            else:
                await self.send_message_to_channel(patient_channel,
                    {
                        'type':'doctor-confirm-order',
                        'flag':False,
                        'status':200,
                        'message':'The doctor has not received order',
                        'doctor_id':await database_sync_to_async(lambda:self.user.doctor_id)(),
                        'doctor_name':await database_sync_to_async(lambda:self.user.base_user.get_full_name)()
                    }               
                )    

        elif data['type']=='disconnect':
            await self.websocket_disconnect()
            
            # await self.send(json.dumps({
            #     "data": {
            #         "message:":"Confirming Order!",
            #         "patient_id":
            #         "status":200
            #     },
            # }))   
        

    async def send_message_to_channel(self,channel_name, data):
      
        channel_layer = get_channel_layer()
        # print(async_to_sync(channel_layer.channel_layer.group_channel_layer.group_channel_layer.has_channel)(channel_name))
        await channel_layer.send(channel_name, {
            'type': 'chat',
            'data':{**data},
        })
        

        
        
    async def chat(self,event):
        
        data = event["data"]
        
        await self.send(text_data=json.dumps(data))

def get_channel_from_connect_table(user_id,flag):
    if flag=='doctor':
        return ConnectDoctor.objects.get(doctor__doctor_id=user_id).doctor_channel
    else:
        return ConnectDoctor.objects.get(patient__patient_id=user_id).patient_channel

@database_sync_to_async
def get_doctors(data):
    
    address=data.pop('address')
    department=data.pop('de_id')
    district=address.get('district')
    city=address.get('city')
    
    addresses=Address.objects.filter(
        district__iregex=f"{district}",
        city__iregex=f"{city}"
    )
    
    #filter doctors is free
    doctors=Doctor.objects.filter(
        is_receive=True,
        departments__de_id=department,
        base_user__address__in=addresses
    )
    if len(doctors)==0:
        return {
            'flag':False,
            'status':200,
            'message':'No doctors'
        }
    else:
        doctors_data=DoctorAppointmentsSerializer(doctors,many=True).data
        
        data=[]
        for doctor_data in doctors_data:
            data.append(dict(doctor_data))    
        return {'doctors':data,'flag':True,'status':200}

@database_sync_to_async
def cancel_order(data):
    patient_id=data.get('patient_id')
    conversation=ConnectDoctor.objects.filter(patient__patient_id=patient_id)
    if len(conversation)>0:
        conversation=conversation[0]
        patient_id=conversation.patient_id
        doctor_channel=conversation.doctor_channel
        conversation.patient_id=None
        conversation.patient_channel=None
        conversation.save()
    return {'flag':True,'status':200,'message':"cancel order successfully!"},{'doctor_channel':doctor_channel,'patient_id':patient_id}

from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.channel_layer.group_add(
            "chat",  # Group name
            self.channel_name  # Channel name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            "chat",  # Group name
            self.channel_name  # Channel name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = text_data_json['user']
        await self.channel_layer.group_send(
            "chat",  # Group name
            {
                "type": "chat.message",
                "message": message,
                "user": user
            }
        )

    async def chat_message(self, event):
        message = event["message"]
        user = event["user"]
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user
        }))

@database_sync_to_async
def create_or_update_conversation(user,channel_name,flag='doctor'):
    if flag=='doctor':
            # await database_sync_to_async(lambda:ConnectDoctor.objects.filter(doctor=self.user).delete())()
        try:
            conversation=ConnectDoctor.objects.get(
                doctor=user
            )
        except:
            conversation=None
        #create doctor
        if conversation is None:
            conversation=ConnectDoctor.objects.create(
                doctor=user,
                doctor_channel=channel_name   
            )
        #update doctor
        else:
            conversation.doctor_channel=channel_name
            conversation.save()
    else:
        print("vao day")
        try:
            conversation=ConnectDoctor.objects.get(
                patient=user
            )
        except:
            conversation=None        

        if not conversation is None:
            conversation.patient_channel=channel_name
            conversation.save()