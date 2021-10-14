import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import os
import random

def initialize_firestore():
    """
    Create database connection
    """

    # Setup Google Cloud Key - The json file is obtained by going to 
    # Project Settings, Service Accounts, Create Service Account, and then
    # Generate New Private Key
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]  = "animal-dict-firebase-adminsdk-k7cse-0357afab83.json"

    # Use the application default credentials.  The projectID is obtianed 
    # by going to Project Settings and then General.
    cred = credentials.ApplicationDefault()
    firebase_admin.initialize_app(cred, {
        'projectId': 'animal-dict',
    })

    # Get reference to database
    db = firestore.client()
    return db


def get_rand_animal(db):
    '''
    This wil grab any animal name and fact about that animal at random and print those both to the screen
    '''
    name_list = db.collection("animal_facts").get() # get list of animal names
    name = random.choice(name_list) # pick a random name from list
    animal_day = name.id # save name to var

    print("") # print name of random animal to user
    print(f"The random animal is a {animal_day.capitalize()}")
    print(f"Here is a cool fact about the {animal_day.capitalize()}")
    print("")

    fact_list = db.collection(u"animal_facts").document(animal_day) # get random fact list attached to animal name we pulled from above.
    get_list = fact_list.get().to_dict() # take that list into a dict
    random_fact = random.choice(list(get_list.values())) # pick a random fact ffrom dict
    print(random_fact) # print random fact

def search_animals(db):
    '''
    Search the database in multiple ways.
    '''


    print("Select Query")
    print("1) Show All Animals")
    print("2) Show Animal By First Letter")        
    choice = input("> ")
    print()

    # Build and execute the query based on the request made
    if choice == "1":
        results = db.collection("animal_facts").get()
    elif choice == "2":
        results = db.collection("animal_facts").get()
    elif choice == "3":
        results = db.collection("animal_facts").get()
    else:
        print("Invalid Selection")
        return
    
    # Display all the results from any of the queries
    print("")
    print("Search Results")
    print(f"{'Name':^30}")
    for result in results:
        data = result.to_dict()
        print(f"{result.id:^30}")
       

def add_new_animal(db):
    '''
    Prompt the user for a new item to add to the inventory database.  The
    item name must be unique (firestore document id).  
    '''

    name = input("Animal Name: ")
    fact = input("Intresting Fact: ")
    
    

    # Check for an already existing item by the same name.
    # The document ID must be unique in Firestore.
    result = db.collection("animal_facts").document(name).get()
    if result.exists:
      print("animal already exists!")
      return

    # Build a dictionary to hold the contents of the firestore document.
    data = {"Intresting Fact": fact}
    db.collection("animal_facts").document(name).set(data)
    # # Save this in the log collection in Firestore       
    log_transaction(db, f"Added {name} with intresting fact {fact}")



def log_transaction(db, message):
    '''
    Save a message with current timestamp to the log collection in the
    Firestore database.
    '''
    data = {"message":message ,"timestamp": firestore.SERVER_TIMESTAMP}
    db.collection("log").add(data)


def main():
    db = initialize_firestore()
    choice = None
    while choice != "0":
        print()
        print("0) Exit")
        print("1) See a random Animal!")
        print("2) Search all Animals")
        choice = input(f"> ")
        print()
        if choice == "1":
            get_rand_animal(db)
        elif choice == "2":
            search_animals(db)
        elif choice == "3":
            add_new_animal(db)                    

if __name__ == "__main__":
    main()
