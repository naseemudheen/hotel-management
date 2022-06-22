# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from account.models import Account 
# from notifications import notify
 
# @receiver(post_save, sender=Account)
# def create_profile(sender, instance, created, **kwargs):
#     print("user is created--------------------------------------------------------------------------------")

#     if created:
#         # notify.send(instance, verb=’was saved’) 
#         pass
  
# # @receiver(post_save, sender=User)
# # def save_profile(sender, instance, **kwargs):
# #         instance.profile.save()

# # from django.db.models.signals import post_save 
# # from myapp.models import MyModel
# # def my_handler(sender, instance, created, **kwargs):
# #      notify.send(instance, verb=’was saved’) 
# #      post_save.connect(my_handler, sender=MyModel)