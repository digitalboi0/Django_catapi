from django.shortcuts import render
import requests
from datetime import datetime, timezone
from rest_framework.response import Response
from rest_framework import status
import logging
from rest_framework.views import APIView
from decouple import config
from . models import String
from . serializer import ValidateString, StringSerializer
import hashlib
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from collections import Counter
import re
from django.http import Http404

HTTP_422_UNPROCESSABLE_ENTITY = 422


# Create your views here.

logger = logging.getLogger(__name__)

EMAIL = config("Email")
NAME = config("Name")
STACK = config("Stack")

CAT_URL = config("Api_url")
REQUEST_TIMEOUT = config("Timeout", cast=int)

class Userprofile(APIView):
    def get(self, request):
        response_data = {
            'status': "success",
            'user': {
                "email": EMAIL,
                "name": NAME,
                "stack":  STACK
                
            },
            "timestamp" : datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "fact" : ""
            
        }
        try:
            response = requests.get(CAT_URL, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            api_response = response.json()
            api_fact = api_response.get('fact', 'Cats are wonderful pets')
            
            response_data["fact"] = api_fact
        except requests.exceptions.RequestException as e:
            logger.error(f"Cat api failed: {str(e)} ")    
            response_data["fact"] = "cats are greats but api is unreachable"
        except ValueError:
            logger.error("api didnt return as a valid json")
            response_data["fact"] = "cats are still great but api didnt return a valid json"
         
        return Response(response_data, status=status.HTTP_200_OK)    
            
class String_Properties:
    def stringproperities(self, value):
        
        if not isinstance(value, str):
            raise ValidationError ("value must be a string")
        
        cleaned_value = value.lower()
        length = len(value)
        sha256_hash = hashlib.sha256(value.encode("utf-8")).hexdigest()
        unique_characters = len(set(value))      
        is_palindrome = cleaned_value == cleaned_value[::-1]
        word_count = len(value.split())
        character_frequency_map  = dict(Counter(value))
        
        
        return {
            
            "length" : length,
            "sha256_hash" : sha256_hash,
            'unique_characters' : unique_characters,
            "is_palindrome" : is_palindrome,
            "word_count" : word_count,
            "character_frequency_map" : character_frequency_map
            
            }
        
class create_string(APIView):
    def post(self, request):
        input_serializer =  ValidateString(data=request.data)
        if not input_serializer.is_valid():
            return Response (input_serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
        string_value = input_serializer.validated_data["value"]
        
        if not input_serializer.is_valid():
            return Response( {"error": "Invalid request body or missing 'value' field"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            existing_instance = String.objects.get(value=string_value)
            return Response (
                {"error" : "String already exists in the system"},
                status=status.HTTP_409_CONFLICT
            )
        except String.DoesNotExist:
            pass
        
        properties = String_Properties().stringproperities(string_value)
        
        new_string = String(
            value = string_value,
            id = properties["sha256_hash"],
            length = properties["length"],
            sha256_hash = properties['sha256_hash'],
            is_palindrome = properties['is_palindrome'],
            unique_characters = properties['unique_characters'],
            word_count = properties["word_count"],
            character_frequency_map = properties['character_frequency_map']
        )
        
        
        new_string.save()
        
        output_json = StringSerializer(new_string)
        
        return Response(output_json.data, status=status.HTTP_201_CREATED)
 
class get_string(APIView):
    def get_string(self, string):
        try:
            object = String.objects.get(value=string)
            return object
        except String.DoesNotExist:
            return Response(
                {"error": "String does not exist in the system"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        
    def get(self, request, string_value):
            instance = self.get_string(string_value)
            serializer = StringSerializer(instance)
            return Response (serializer.data, status=status.HTTP_200_OK)

class   string_list(APIView):
    def get(self, request):
        queryset = String.objects.all()
        is_palindrome = request.query_params.get("is_palindrome", None)
        min_length = request.query_params.get("min_length", None)
        max_length = request.query_params.get("max_length", None)
        word_count = request.query_params.get("word_count", None)
        contains_character = request.query_params.get("contains_character", None)
        
        
        
        if is_palindrome is not None:
            is_palindrome_bool = is_palindrome.lower() ==  "true"
            queryset =  queryset.filter(is_palindrome=is_palindrome_bool)
            
            
            
        if min_length is not None:
            try:
                min_length = int(min_length)
                queryset = queryset.filter(length__gte=min_length)
            except ValueError:
                return Response({"error": "Invalid query parameter values or types"}, status=status.HTTP_400_BAD_REQUEST)  
            
            
        if max_length is not None:
            try:
                max_length = int(max_length)
                queryset = queryset.filter(length__lte=max_length)
            except ValueError:
                return Response(
                    {"error": "Invalid query parameter values or types"}, status=status.HTTP_400_BAD_REQUEST
                )
                
                
                
        if word_count is not None:
            try:
                word_count = int(word_count)
                queryset = queryset.filter(word_count=word_count)
            except ValueError:
                return Response({
                    "error": "Invalid query parameter values or types"
                }, status=status.HTTP_400_BAD_REQUEST)       
                
                
        if contains_character  is not None:
            queryset = queryset.filter(value__icontains=contains_character)       
            
            
        serializer = StringSerializer(queryset, many=True)     
       
       
        Response_date = {
           "data" : serializer.data,
           "count" : queryset.count(),
           'filters_applied' : {
               "is_palindrome" : is_palindrome,
               "min_length" : min_length,
               "max_length" : max_length,
               "word_count" : word_count,
               "contains_character" : contains_character
               
           }
       }
       
       
        return Response(Response_date, status=status.HTTP_200_OK)
   
   
class delete_string(APIView):
    def get_data(self, string):
        try:
            object = String.objects.get(value=string)
            return object
        except String.DoesNotExist:
            raise Http404
           
            
    def delete(self, request, string_value):
        try:
            instance =  self.get_data(string_value)
        except Http404:
            return Response(
                {"error": "String does not exist in the system"},
                status=status.HTTP_404_NOT_FOUND)
            
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)  
    
    def get(self, request, string_value):
        try:
            instance = self.get_data(string_value)
        except Http404:
            
             return Response(
                {"error": "String does not exist in the system"},
                status=status.HTTP_404_NOT_FOUND)
                
                
        serializer = StringSerializer(instance)
        return Response (serializer.data, status=status.HTTP_200_OK)   
            
           
    
       
    
    
    
class natural_lang(APIView):
    def get(self,request):
        query =  request.query_params.get("query", None)
        if query == None:
            return Response(
                {"error": "Unable to parse natural language query"}, status=status.HTTP_400_BAD_REQUEST
            )    
            
        parsed_filters = {}
        cleaned_query =  query.lower()
        
         # Example: "all single word palindromic strings"
         
        if  "single word" in cleaned_query or "single-word" in cleaned_query:
             parsed_filters["word_count"] = 1
        if "palindromic" in cleaned_query or "palindrome" in cleaned_query:
             parsed_filters["is_palindrome"] = True
             
          # Example: "strings longer than 10 characters"
        if "longer than" in cleaned_query:
              
              match = re.search(r"than\s+(\d+)", cleaned_query)
              if match:
                  try:
                      min_len = int(match.group(1)) + 1
                      parsed_filters['min_length'] = min_len
                  except ValueError:
                      pass
                  
                  
         # Example: "strings containing the letter z"
         
        contains_match = re.search(r"containing.*letter\s+([a-z])", cleaned_query)
        if contains_match:
            char = contains_match.group(1)
            parsed_filters['contains_character'] = char
            
        shorter_than_match = re.search(r"shorter\s+than\s+(\d+)", cleaned_query)
        if shorter_than_match:
            try:
                max_len = int(shorter_than_match.group(1)) - 1 
                parsed_filters['max_length'] = max_len
            except ValueError:
                pass    
            
        less_than_match = re.search(r"less\s+than\s+(\d+)", cleaned_query)
        if less_than_match:
            try:
                max_len = int(less_than_match.group(1)) - 1 
                parsed_filters['max_length'] = max_len 
            except ValueError:
                pass
        
            
        min_len = parsed_filters.get('min_length')
        max_len = parsed_filters.get('max_length')    
        
        if min_len is not None and max_len is not None and min_len > max_len:
            return Response( {"error": "Query parsed but resulted in conflicting filters"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
            
        
        
        
        if not parsed_filters:
            return Response(
                 {"error": "Unable to parse natural language query"}, status=status.HTTP_400_BAD_REQUEST
            )      
                  
        queryset = String.objects.all()
       
       
        if 'is_palindrome' in parsed_filters:
            queryset = queryset.filter(is_palindrome=parsed_filters['is_palindrome'])
        if 'word_count' in parsed_filters:
            queryset = queryset.filter(word_count=parsed_filters['word_count'])
        if 'min_length' in parsed_filters:
            queryset = queryset.filter(length__gte=parsed_filters['min_length'])
        if 'contains_character' in parsed_filters:
            queryset = queryset.filter(value__icontains=parsed_filters['contains_character'])                       
            
            
            
            
        serializer = StringSerializer(queryset, many=True)
       
       
        response_data = {
            "data": serializer.data,
            "count": queryset.count(),
            "interpreted_query": {
                "original": query,
                "parsed_filters": parsed_filters
            }
        }

        return Response(response_data, status=status.HTTP_200_OK)     