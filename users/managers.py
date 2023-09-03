from django.contrib.auth.base_user import BaseUserManager
# from django.utils.translation import ugettext_lazy as _
from django.utils.translation import gettext_lazy as _



class UserManager(BaseUserManager):
  """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
  """
  def create_user_bulk(self,name,roll_no, email,semester,department, password, **extra_fields):
      """
      Create and save a User with the given email and password.
      """
      if not roll_no:
        raise ValueError('The Roll Number must be set')

      if not email:
        raise ValueError('The Email must be set')

      email = self.normalize_email(email)
      
      user = self.model(roll_no=roll_no,name = name, email=email,semester= semester,department= department, **extra_fields)
      user.set_password(password)
      user.save()
      return user

  def create_user(self, roll_no, email, password, **extra_fields):
      """
      Create and save a User with the given email and password.
      """
      if not roll_no:
        raise ValueError('The Roll Number must be set')

      if not email:
        raise ValueError('The Email must be set')

      email = self.normalize_email(email)
      
      user = self.model(roll_no=roll_no, email=email, **extra_fields)
      user.set_password(password)
      user.save()
      return user
  def create_superuser(self,roll_no, email, password, **extra_fields):
      """
      Create and save a SuperUser with the given email and password.
      """
      extra_fields.setdefault('is_staff', True)
      extra_fields.setdefault('is_superuser', True)
      extra_fields.setdefault('is_active', True)

      if extra_fields.get('is_staff') is not True:
          raise ValueError(_('Superuser must have is_staff=True.'))
      if extra_fields.get('is_superuser') is not True:
          raise ValueError(_('Superuser must have is_superuser=True.'))

      return self.create_user(roll_no, email, password, **extra_fields)

# to create super user uncomment above user 

# to create bulkUsers uncomment below code


  # def create_superuser(self,roll_no, email, password, **extra_fields):
  #   """
  #   Create and save a SuperUser with the given email and password.
  #   """
  #   extra_fields.setdefault('is_staff', False)
  #   extra_fields.setdefault('is_superuser', False)
  #   extra_fields.setdefault('is_active', True)

  #   # if extra_fields.get('is_staff') is not True:
  #   #     raise ValueError(_('Superuser must have is_staff=True.'))
  #   # if extra_fields.get('is_superuser') is not True:
  #   #     raise ValueError(_('Superuser must have is_superuser=True.'))
  #   import csv

  #   with open(r'C:\Users\Dell\Desktop\FACES-22_E\backend\users\data.csv', newline='') as csvfile:
  #     spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')

  #     for row in spamreader:          
          
  #         # AD, 5, 5@gmail.com, Comp, 5, 13pCqSnayL,
  #         # row.pop()
  #         #print(row)
  #         row.pop(6)
  #         print(row)
  #         [name, roll_no, email, department, semester,password] = row
  #         # roll_no=
  #         roll_no = roll_no.replace(',','')
  #         roll_no = roll_no.replace(' ','')
  #         semester = semester.replace(',','')
  #         semester = semester.replace(' ','')
  #         password = password.replace(',','')
  #         password = password.replace(' ','')
  #         department = department.replace(',','')
  #         department = department.replace(' ','')
  #         email = email.replace(',','')
  #         email = email.replace(' ','')
  #         name = name.replace(',','')
  #         print(password)
  #         # if you want to createsuperuser create_user(....) instead of create_user_bulk(...) and add true to superuser and staff and comment above code. 56-66 line
  #         self.create_user_bulk(name,roll_no, email,semester,department, password,**extra_fields)
  #     # create_users()    
  #   return self.create_user_bulk(name,roll_no, email,semester,department, password,**extra_fields)
