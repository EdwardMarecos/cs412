from django.db import models
import datetime
from datetime import datetime


# Create your models here.

class Voter(models.Model):
    '''
    Store/represent the data from one voter.
        *    Last Name
        *    First Name
        *    Residential Address - Street Number
        *    Residential Address - Street Name
        *    Residential Address - Apartment Number
        *    Residential Address - Zip Code
        *    Date of Birth
        *    Date of Registration
        *    Party Affiliation
        *    Precinct Number

        the following  indicate whether or not a given voter participated in several recent elections
        *    v20state
        *    v21town
        *    v21primary
        *    v22general
        *    v23town
    '''


    # identification
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    dob = models.DateField()

    # address
    address_num = models.IntegerField()
    address_street = models.TextField()
    address_apt_num = models.CharField(max_length=10, null=True, blank=True)  # optional, can include letters
    address_zipcode = models.IntegerField()

    # location
    precinct = models.CharField(max_length=3)

    # voting data
    reg_date = models.DateField(null=True)  # error on a non nullable field, kinda confused cause dob is non nullable and ok but wtvr
    party = models.CharField(max_length=50)
    v20state = models.BooleanField()
    v21town = models.BooleanField()
    v21primary = models.BooleanField()
    v22general = models.BooleanField()
    v23town = models.BooleanField()

    # voting score
    voter_score = models.IntegerField()

    def __str__(self):
        return f"{self.first_name} {self.last_name} - Precinct {self.precinct}"
    
def load_data():
    '''Function to load data records from CSV file into Django model instances.'''
    filename = r"C:\Users\edmar\Desktop\cs412\hw10\newton_voters.csv"
    f = open(filename)
    f.readline() # discard headers

    for line in f:

        #provide protection around code that may be cursed
        try:
            fields = line.split(',')

            # Create a new instance of Voter object with this record from CSV
            voter = Voter(
                last_name=fields[1],  # String, no conversion needed
                first_name=fields[2],  # String, no conversion needed
                address_num=int(fields[3]) if fields[3] else None,  # Convert to integer
                address_street=fields[4],  # String, no conversion needed
                address_apt_num=fields[5] if fields[5] else None,  # Optional, keep as string
                address_zipcode=int(fields[6]) if fields[6] else None,  # Convert to integer
                dob=datetime.strptime(fields[7], '%m/%d/%Y').date() if fields[7] else None,  # Convert to date
                reg_date=datetime.strptime(fields[8], '%m/%d/%Y').date() if fields[8] else None,  # Convert to date
                party=fields[9],  # String, no conversion needed
                precinct=fields[10],  # leave as is
                v20state=fields[11].strip().upper() == 'TRUE',  # Convert to boolean
                v21town=fields[12].strip().upper() == 'TRUE',  # Convert to boolean
                v21primary=fields[13].strip().upper() == 'TRUE',  # Convert to boolean
                v22general=fields[14].strip().upper() == 'TRUE',  # Convert to boolean
                v23town=fields[15].strip().upper() == 'TRUE',  # Convert to boolean
                voter_score=int(fields[16].strip()) if fields[16] else None,  # Convert to integer
            )
            voter.save()  # save this instance to the database
            print(f'Created voter: {voter}')
        except Exception as e:
            print(f"Exception on {fields}: {e}")