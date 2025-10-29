from django.shortcuts import render
from .models import Country
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import logging
from django.utils import timezone
from decimal import Decimal, InvalidOperation
import random
import requests
from . serializer import CountrySerializer
import os
from django.http import FileResponse, HttpResponseNotFound
from django.conf import settings
from PIL import Image, ImageDraw, ImageFont
from decouple import config
from django.db.models import Max



# Create your views here.
COUNTRY_URL = config("COUNTRY_URL")
RATE_URL = config("RATE_URL")
TIME_OUT = config("timeout", cast=int)

logger = logging.getLogger(__name__)

class RefreshCountryView(APIView):
    def post(self, request, *args, **kwargs):
        try:
            logger.info("fetching countries data from url")
            countries_response = requests.get(COUNTRY_URL, timeout=TIME_OUT)
            countries_response.raise_for_status()
            countries_data =  countries_response.json()
            logger.info(f"data fetched from {len(countries_data)} the url")
            
            
            logger.info("fetching rate from url")
            exchange_rate_response = requests.get(RATE_URL, timeout=TIME_OUT)
            exchange_rate_response.raise_for_status()
            
            exchange_data = exchange_rate_response.json()
            er = exchange_data.get("rates", {})
            logger.info(f"fetched {len(exchange_data)}")
            
            
            
           
            
            updated_count = 0
            created_count = 0
            skipped_count = 0
            
            last_refreshed_at =  timezone.now()
            
        
            if not isinstance(countries_data, list):
                return Response(
                    {"error": "Invalid data format from external API"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            for country_data in countries_data:
                name = country_data.get("name")
                if not name:
                    logger.warning("country name not found skipping")
                    skipped_count +=1
                    continue
                capital = country_data.get("capital")
                region = country_data.get("region")
                population = country_data.get("population", 0)
                flag_url = country_data.get("flag")
                
                currency_code = None
                exchange_rate = None
                
                currencies = country_data.get("currencies", [])
                if currencies and isinstance(currencies, list):
                    first_currency_dict =  currencies[0] if len(currencies) > 0 and isinstance(currencies[0], dict) else None
                    if first_currency_dict:
                        currency_code = first_currency_dict.get("code")
                   
                        
                        
                        
                if currency_code:
                    rate_value = er.get(currency_code)
                    if rate_value is not None:
                        try:
                            exchange_rate = rate_value
                        except(ValueError, InvalidOperation) as e:
                            logger.warning(f"invalid exchange rate for {currency_code}: {rate_value}. error {e} ")   
                            exchange_rate = None 
                            
                
                
                estimated_gdp = None
                if population > 0 and exchange_rate is not None and exchange_rate > 0:
                    random_no = Decimal(random.randint(1000, 2000))
                    pop = Decimal(population)
                    er_t =Decimal(exchange_rate)
                    try:
                        estimated_gdp = pop * random_no / er_t
                        estimated_gdp = Decimal(estimated_gdp)
                    except(ValueError, ZeroDivisionError, InvalidOperation, OverflowError) as e:
                        logger.warning(f"error get estimated_gdp for {name}: error {e}")
                        estimated_gdp = None
                        
                        
            
                try:
                    country_obj, created = Country.objects.update_or_create(name=name, defaults={
                        "capital" : capital,
                        "region" : region,
                        "population" : population,
                        "currency_code" : currency_code,
                        "exchange_rate" : exchange_rate,
                        "estimated_gdp" : estimated_gdp,
                        "flag_url" : flag_url,
                        "last_refreshed_at" : last_refreshed_at,
                    }) 
                    if created:
                        created_count +=1
                        logger.info(f"created new for country record for {name}")
                    else:
                        updated_count +=1
                        logger.info(f"updated for country record for {name}")    
                except Exception as e:
                    logger.error(f"error creating/updating record for country {name}: {e}")
                    pass
                
                
            logger.info(f"refresh completed update {updated_count} time, created {created_count} times, and skipped {skipped_count} time")
            try:
                generate_summary_image()
                logger.info("Summary image generated successfully.")
            except Exception as e:
                logger.error(f"Failed to generate summary image, but refresh succeeded: {e}")
                
            return Response(
                    {
                        "message" : "countries refreshed completed",
                        "countries_updated" : updated_count,
                        "countries_created" : created_count,
                        "countries_skipped" : skipped_count,
                        "time_refreshed" : last_refreshed_at
                        
                        
                        
                    }, status= status.HTTP_200_OK
                ) 
        except requests.exceptions.RequestException as e:   
            logger.error(f"error connecting to api {e}")
            return Response(
                {"error": "external data source unvailable", "details": str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )     
                
                
        except Exception as e:
            logger.critical(f"Unexpected error during country refresh: {e}", exc_info=True)
            return Response(
                {"error": "Internal server error during refresh", "details": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )     
       
            
            
class GetCountriesView(APIView):
    def get(self, request, *args, **kwargs):
        region = request.query_params.get("region", None)
        currency_code = request.query_params.get("currency", None)
        sort_order = request.query_params.get("sort", None)
        queryset = Country.objects.all()
        if region is not None:
            queryset = queryset.filter(region=region)
        if currency_code is not None:
            queryset = queryset.filter(currency_code=currency_code)
        ordering = None
        if sort_order is not None:
            if sort_order == "gdp_desc":
                ordering = ["-estimated_gdp"]
            elif sort_order == 'gdp_asc':
                 ordering = ['estimated_gdp']
            elif sort_order == 'name_asc':
                ordering = ['name']
            elif sort_order == 'name_desc':
                ordering = ['-name']
            elif sort_order == 'population_desc':
                ordering = ['-population']
            elif sort_order == 'population_asc':
                ordering = ['population']            
                
                
                
                
                
            if ordering is not None:
                queryset =queryset.order_by(*ordering)   
        
        temp_data = CountrySerializer(queryset, many=True)
        return Response(
            temp_data.data, status=status.HTTP_200_OK
        )   
        
        
 
 
class GetCountryView(APIView):
    
    def get(self, request, *args, **kwargs):
        name = kwargs.get('name')
        
        try:
            logger.info(f"attempting to get data by {name}")
            try:
                country_data = Country.objects.get(name__iexact=name)
                logger.info(f"records found for {name}")
            except Country.DoesNotExist:
                logger.error(f"no record found {name}")
                return Response(
                    {"error": "country not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
             
            cu_data = CountrySerializer(country_data,)
            return Response(cu_data.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.critical(f"Unexpected error retrieving country '{name}': {e}", exc_info=True)
            return Response(
                {"error": "Internal server error retrieving country"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    def delete(self, request, *args, **kwargs):
        name = kwargs.get('name')
        try:
            logger.info(f'get {name} records so it can be deleted')
            country_to_deleted = Country.objects.get(name__iexact=name)
        except Country.DoesNotExist:
            logger.critical(f"no record found for {name}")
            return Response(
                {"error": "country doesnt exist"},
                status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            logger.critical(f"error occured deleting the data {e}")
            return Response(
                {"error": "error occured during the deletion"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
        country_to_deleted.delete() 
        return Response(
            {"message": "country deleted"},
            status=status.HTTP_200_OK
        )   
            
class GetCountryStatus(APIView):
    def get(self, request, *args, **kwargs):
        try:
            logger.debug("Fetching status information.")
            total_countries = Country.objects.count()
            logger.debug(f"Total countries count: {total_countries}")
            aggregate_result = Country.objects.aggregate(latest=Max('last_refreshed_at'))
            last_refreshed_at = aggregate_result['latest']
            logger.debug(f"Latest refresh timestamp from DB (aggregate result): {aggregate_result}")
            logger.debug(f"Latest refresh timestamp extracted: {last_refreshed_at}")
            last_refreshed_at_iso = last_refreshed_at.isoformat() if last_refreshed_at else None
            
            response_data = {
                "total_countries": total_countries,
                "last_refreshed_at": last_refreshed_at_iso 
            }
            logger.info(f"Status retrieved: Total={response_data['total_countries']}, LastRefresh={response_data['last_refreshed_at']}")
            return Response(response_data, status=status.HTTP_200_OK)
        
        except Exception as e:
            logger.critical(f"Unexpected error retrieving status: {e}", exc_info=True)
            return Response(
                {"error": "Internal server error retrieving status"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            
class GetImageSummery(APIView):
    IMAGE_FILENAME = "summary.png"
    CACHE_DIR_NAME = "cache"  
    IMAGE_PATH = os.path.join(settings.BASE_DIR, CACHE_DIR_NAME, IMAGE_FILENAME)   
    def get(self,request, *args, **kwargs):
        try:
            logger.debug(f"getting image from path{self.IMAGE_PATH}")
            if os.path.exists(self.IMAGE_PATH):
                logger.info(f"Image found at {self.IMAGE_PATH}. Serving...")
                return FileResponse(
                    open(self.IMAGE_PATH, "rb"), content_type="image/png"
                    
                )
            else:
                logger.warning(f"Image not found at {self.IMAGE_PATH}. Returning 404.")
                return Response(
                    {"error": "Summary image not found"},
                    status=status.HTTP_404_NOT_FOUND
                )
        except FileNotFoundError:
            logger.error(f"FileNotFoundError: Image file could not be opened/read: {self.IMAGE_PATH}")
            return Response(
                {"error": "Summary image not found"},
                status=status.HTTP_404_NOT_FOUND)
        except PermissionError:    
            logger.error(f"PermissionError: Insufficient permissions to read image file: {self.IMAGE_PATH}")
            return Response(
                {"error": "Permission denied accessing summary image"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR # Or 403 Forbidden?
            )
            

        except Exception as e:
            logger.critical(f"Unexpected error serving image '{self.IMAGE_PATH}': {e}", exc_info=True)
            return Response(
                {"error": "Internal server error serving image"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
   
    



CACHE_DIR = os.path.join(settings.BASE_DIR, 'cache')
IMAGE_FILENAME = 'summary.png'
IMAGE_PATH = os.path.join(CACHE_DIR, IMAGE_FILENAME)


IMAGE_WIDTH = 800
IMAGE_HEIGHT = 600

def generate_summary_image():
   
    try:
        logger.info("Starting summary image generation...")

       
        os.makedirs(CACHE_DIR, exist_ok=True)
        logger.debug(f"Ensured cache directory exists: {CACHE_DIR}")


        total_countries = Country.objects.count()
        logger.debug(f"Total countries fetched: {total_countries}")


        from django.db.models import Max
        aggregate_result = Country.objects.aggregate(latest=Max('last_refreshed_at'))
        last_refresh_timestamp = aggregate_result['latest']

        if last_refresh_timestamp is None:
            logger.warning("No last_refreshed_at timestamp found in Country records for image. Using current time.")
            last_refresh_timestamp = timezone.now()

        logger.debug(f"Last refresh timestamp determined: {last_refresh_timestamp}")


        top_gdp_countries = Country.objects.exclude(estimated_gdp__isnull=True).order_by('-estimated_gdp')[:5]
        logger.debug(f"Top 5 GDP countries fetched: {[c.name for c in top_gdp_countries]}")


        image = Image.new('RGB', (IMAGE_WIDTH, IMAGE_HEIGHT), color=(255, 255, 255)) 
        draw = ImageDraw.Draw(image)
        logger.debug("Image canvas created.")


        font_large = None
        font_medium = None
        font_small = None
        try:

            font_large = ImageFont.truetype("arial.ttf", size=28)
            font_medium = ImageFont.truetype("arial.ttf", size=22)
            font_small = ImageFont.truetype("arial.ttf", size=18)
            logger.debug("Custom fonts loaded successfully.")
        except OSError as e:

            logger.warning(f"Specific font not found, using default font. Error: {e}")
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()


        y_offset = 50
        line_height_large = 35
        line_height_medium = 30
        line_height_small = 25

        draw.text((50, y_offset), "Country Data Summary", fill=(0, 0, 0), font=font_large)
        y_offset += line_height_large + 10


        draw.text((50, y_offset), f"Total Countries: {total_countries}", fill=(0, 0, 0), font=font_medium)
        y_offset += line_height_medium


        if timezone.is_naive(last_refresh_timestamp):
             formatted_timestamp = timezone.make_aware(last_refresh_timestamp).strftime("%Y-%m-%d %H:%M:%S %Z")
        else:
             formatted_timestamp = last_refresh_timestamp.strftime("%Y-%m-%d %H:%M:%S %Z")

        draw.text((50, y_offset), f"Last Refresh: {formatted_timestamp}", fill=(0, 0, 0), font=font_medium)
        y_offset += line_height_medium + 20


        draw.text((50, y_offset), "Top 5 Countries by GDP:", fill=(0, 0, 0), font=font_large)
        y_offset += line_height_large


        if top_gdp_countries:
            for country in top_gdp_countries:

                if country.estimated_gdp is not None:
                    try:

                        gdp_formatted = f"{country.estimated_gdp:,.2f}"
                    except (ValueError, TypeError) as e:
                        logger.warning(f"Error formatting GDP for {country.name}: {e}")
                        gdp_formatted = "N/A (Format Error)"
                else:
                    gdp_formatted = "N/A"

                text_to_draw = f"{country.name}: {gdp_formatted}"
                draw.text((70, y_offset), text_to_draw, fill=(50, 50, 50), font=font_small) 
                y_offset += line_height_small


                if y_offset > IMAGE_HEIGHT - 30:
                    logger.debug("Reached near bottom of image, stopping list drawing.")
                    break
        else:
            draw.text((70, y_offset), "No countries with calculated GDP found.", fill=(100, 100, 100), font=font_small)
            y_offset += line_height_small



        image.save(IMAGE_PATH)
        logger.info(f"Summary image generated successfully and saved to {IMAGE_PATH}")

    except Exception as e:
        logger.critical(f"Failed to generate summary image: {e}", exc_info=True)
 

                
              
        
               
        
    
    
        
        
                        
                           
                    
                    
                
              
                
            
