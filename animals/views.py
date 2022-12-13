from django import views
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status, permissions

from .models import Animal, Page #, Contributor
from .serializers import AnimalSerializer
from rest_framework.generics import GenericAPIView, CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateAPIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin

import requests
      

# Create your views here.
def loginUser(request):
    
    if request.user.is_authenticated:
        return redirect('animals:animals')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('animals:home')
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})

    return render(request, 'login.html')

def changePW(request):
    if request.method == 'POST':
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        
        try:
            user = User.objects.get(username=username)
            
            if username and password1 and password2:
                if password1 == password2:
                    user.set_password(password1)
                    user.save()
                    return redirect('animals:home')
                return render(request, 'change_password.html', {'error': 'Passwords not same'})
        except:
            return render(request, 'change_password.html', {'error': 'No matching details'})
    return render(request, 'change_password.html')

def logoutUser(request):
    logout(request)
    return redirect('animals:home')

# @login_required(login_url='animals:login')
def homeView(request):
    home = Page.objects.latest('updated') 
    home.home_page_views = home.home_page_views + 1
    home.save() 
    
    "#Number of visits to this view, as counted in the session variable."
    # num_visits = request.session.get('num_visits', 1)
    # request.session['num_visits'] = num_visits + 1

    if request.method == 'POST':
        
        name = request.POST['nameinput']
        name = name.title()
        # print(name)
        url = "https://animaliapi3.p.rapidapi.com/all/{}".format(name)

        headers = {
            'x-rapidapi-host': "animaliapi3.p.rapidapi.com",
            'x-rapidapi-key': "ec3d81a68amsh03ca29edb107ce3p12a3a0jsn39d3eaecb565"
            }

        response = requests.request("GET", url, headers=headers)
        # print(response.text)

        if "Not found" in response.text:
            return render(request, 'home.html', {'name':name, 'error': "not found"})

        elif "Error (500)" in response.text:
            return render(request, 'home.html', {'name':name, 'error': "Server error"})

        return render(request, 'home.html', {'name':name, 'response': response.text})


    return render(request, 'home.html', {'name':'Cheetah', 'home': home})
    

def viewAll(request):
    existing_animals = []
    # all = {}
    animalnames = Animal.objects.values('id', 'name')
    # print(animalnames)
    # print('Total animals already in API: ', len(animalnames))

    for animal in animalnames:
        # print(animal['id'], animal['name'])
        existing_animals.append(animal['name'].lower())
        # all.update({animal['id']: animal['name']})
    # print(all)
    # print('Existing animals: ', existing_animals)
    # repeated_animals = set([x for x in existing_animals if existing_animals.count(x) > 1])
    # To get all classnames
    classname = request.GET.get('classname')
    # print(classname)

    if classname  == None:
        animals = Animal.objects.all()
        animals = animals[:12]

    else:
        animals = Animal.objects.filter(classname=classname)
        animals = animals[:12]

    classes = Animal.objects.values('classname').distinct()  
    # print(classes)
    context = {'classes': classes, 'animals':animals, 'classname': classname, 'total': len(existing_animals)}  # , 'all': all, 'repeated': repeated_animals, 'distinct': len(list(set(existing_animals)))
    return render(request, 'all.html', context)

def viewDetail(request, pk):
    animal = Animal.objects.get(id=pk)
    return render(request, 'detail.html', {'animal': animal})


# @login_required(login_url='animals:login')
# @api_view(['GET','POST'])
# def addAnimal(request):

#     animal = request.data.get('animal')
#     animal_serializer = AnimalSerializer(data=animal)
#     if animal_serializer.is_valid(raise_exception=True):
#         animal_saved = animal_serializer.save()
#         return Response({"success": "Animal '{}' created successfully".format(animal_saved.name)})
#     else:
#         error_details = []
#         for key in animal_serializer.errors.keys():
#             error_details.append({"field": key, "message": animal_serializer.errors[key][0]})

#         data = {
#                 "Error": {
#                     "status": 400,
#                     "message": "Your submitted data was not valid - please correct the below errors",
#                     "error_details": error_details
#                     }
#                 }        
#         return Response(data, status=status.HTTP_400_BAD_REQUEST)

    # if request.user.is_authenticated:
    #     return render(request, 'add.html')

    # return redirect('animals:login')

# Read API endpoints to request using name
class AnimalGetView(APIView):
    # classbased permissions
    # permission to onlyread for unauthenticated users
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, )

    def get(self, request, name=None):
        # if not request.user.is_authenticated:
        #     return redirect('animals:login')
        

        # this is a shorter way to request without using try catch and returns default Not found error message if not found

        # animal = get_object_or_404(Animal.objects.all(), name=name)
        # serializer = AnimalSerializer(animal)
        # return Response({"animal": serializer.data})
        # animals = Animal.objects.all()
        
        # serializer = AnimalSerializer(animals, many=True)
        # return Response({"animals": serializer.data})

        # Try this to return what user is trying to request
        try:
            animal = Animal.objects.get(name=name)
            serializer = AnimalSerializer(animal)
            return Response({"animal": serializer.data})
        except:
            return Response({"detail for {}".format(name): "Not found"})

    
    def put(self, request, name):
        # if not request.user.is_authenticated:
        #     return redirect('animals:login')
        saved_animal = get_object_or_404(Animal.objects.all(), name=name)
        data = request.data.get('animal')
        serializer = AnimalSerializer(instance=saved_animal, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            animal_saved = serializer.save()
        return Response({"success": "Animal '{}' updated successfully".format(animal_saved.name)})

    def delete(self, request, name):
        # if not request.user.is_authenticated:
        #     return redirect('animals:login')
        # Get the object with this pk
        animal = get_object_or_404(Animal.objects.all(), name=name)
        animal.delete()
        return Response({"message": "Animal with id '{}' has been deleted.".format(name)}, status=204)


# using APIView to use ID
class AnimalView(APIView):
    # classbased permissions
    # permission to onlyread for unauthenticated users
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly, )
    
    def get(self, request, pk=None):
        # if not request.user.is_authenticated:
        #     return redirect('animals:login')
        if pk:

            # this is a shorter way to request without using try catch and returns default Not found error message if not found

            # animal = get_object_or_404(Animal.objects.all(), pk=pk)
            # serializer = AnimalSerializer(animal)

            # # animal = Animal.objects.get(pk=pk)
            # # serializer = AnimalSerializer(animal)

            # return Response({"animal": serializer.data})

            # Try this to return what user is trying to request
            try:
                animal = Animal.objects.get(pk=pk)
                serializer = AnimalSerializer(animal)
                return Response({"animal": serializer.data})
            except:
                return Response({"detail for {}".format(pk): "Not found"})

        
        animals = Animal.objects.all().order_by('id')
    
        
        serializer = AnimalSerializer(animals, many=True)
        return Response({"animals": serializer.data})

        
    def post(self, request):
        # if not request.user.is_authenticated:
        #     return redirect('animals:login')

        # To check the animal names
        existing_animals = []
        animalnames = Animal.objects.values('id', 'name')
        # print(animalnames)
        # print('Total animals already in API: ', len(animalnames))

        for animal in animalnames:
            # print(animal['id'], animal['name'])
            existing_animals.append(animal['name'].lower())
        # print('Existing animals: ', existing_animals)

        # get new animals
        new_animals = request.data.get('animals')
        # print('New animals: ', new_animals)
        new_animal = request.data.get('animal')
        # print('New animal: ', new_animal)
        if (new_animals):

            for i in new_animals:
                # print(i)
                name = i['name'].lower()
                if name in existing_animals:
                    new_animals.remove(i)
                    # print(name, 'already exists')


            print('Updated new animal list: ', new_animals)
            # print('starting to add...')
            for i in new_animals:
            #     print(i)

                # Create an animal from the above data
                serializer = AnimalSerializer(data=i)
                if serializer.is_valid(raise_exception=True):
                    animal_saved = serializer.save()
            # print('added')
            return Response({"success": "Animals added successfully"})
        elif(new_animal):
            name = new_animal['name'].lower()
            if name in existing_animals:
                # print(name, 'already exists')
                return Response({"Failed": "{} already exists".format(name)})

            else:
                # print('Adding {} ...'.format(name))
                serializer = AnimalSerializer(data=new_animal)
                if serializer.is_valid(raise_exception=True):
                    animal_saved = serializer.save()
                # print('added')
                return Response({"success": "Animal '{}' added successfully".format(animal_saved.name)})
        

    def put(self, request, pk):
        # if not request.user.is_authenticated:
        #     return redirect('animals:login')
        saved_animal = get_object_or_404(Animal.objects.all(), pk=pk)
        data = request.data.get('animal')
        serializer = AnimalSerializer(instance=saved_animal, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            animal_saved = serializer.save()
        return Response({"success": "Animal '{}' updated successfully".format(animal_saved.name)})

    def delete(self, request, pk):
        # if not request.user.is_authenticated:
        #     return redirect('animals:login')
        # Get the object with this pk
        animal = get_object_or_404(Animal.objects.all(), pk=pk)
        animal.delete()
        return Response({"message": "Animal with id '{}' has been deleted.".format(pk)}, status=204)

# using GenericAPIView instead of APIView
## for all of the below add contributor_id for my to work
# 1 ...for get request ..return a list of all animals that we currently have in our database
# class AnimalView(ListModelMixin, GenericAPIView):
#     queryset = Animal.objects.all()
#     serializer_class = AnimalSerializer

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, *kwargs)

# 2...Provide user with ability to create and animal----GET, POST
# class AnimalView(ListModelMixin, CreateModelMixin, GenericAPIView):
#     queryset = Animal.objects.all()
#     serializer_class = AnimalSerializer

#     def perform_create(self, serializer):
#         contributor = get_object_or_404(Contributor, id=self.request.data.get('contributor_id'))
#         return serializer.save(contributor=contributor)

#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, *kwargs)

#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# 3... without the need to define get and post ----CREATE, GET, 
# class AnimalView(CreateAPIView, ListAPIView):
#     queryset = Animal.objects.all()
#     serializer_class = AnimalSerializer

#     def perform_create(self, serializer):
#         contributor = get_object_or_404(Contributor, id=self.request.data.get('contributor_id'))
#         return serializer.save(contributor=contributor)

# # Combining both creating and listing an animal
# class AnimalView(ListCreateAPIView):
#     queryset = Animal.objects.all()
#     serializer_class = AnimalSerializer
    
#     def perform_create(self, serializer):
#         contributor = get_object_or_404(Contributor, id=self.request.data.get('contributor_id'))
#         return serializer.save(contributor=contributor)

# # This allows only to view single animal using animal id
# # class SingleAnimalView(RetrieveAPIView):  # to allow users to update their animals, provide user with a way to retrieve a single animal
# #     queryset = Animal.objects.all()
# #     serializer_class = AnimalSerializer

# # This allows us to retrieve the animal using id and at the same time update the animal 
# class SingleAnimalView(RetrieveUpdateAPIView):
#     queryset = Animal.objects.all()
#     serializer_class = AnimalSerializer