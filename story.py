x = input("You are in procrastination central, which option do you choose?")
social_media = True
lying_down = True
messy = True
not_smelly = False

def lay_down():
    if(lying_down == False):
        print("Well you are up thats a start.")
    else:
        print("You should probably get up")
        lying_down = False



def on_sm():
    if(social_media == True):
        print("You should probably get off of any social medias (Reddit | Tiktok | X | Meta | Instagram | Youtube)")
    else:
        print("Well this is a good start. Not being on social media and all.")
        social_media = False


def room():
    bedsheets = False
    print("Is your room messy? Be honest with yourself")
    if(messy == True):
        print("Definitely clean up your room. Are your bedsheets messy?")
        if(bedsheets == False):
            print("If your bedsheets haven't been cleaned in over a month, its definitely time to throw them in the washer, along with the pillow-sheets and blankets.")
    else:
        print("Ok room cleaned")
        messy = False

def smells():
    if(not not_smelly):
        print("Yeah definitely make sure that the room doesn't smell.")
        not_smelly = False
    else:
        print("Ok the room isn't smelly")
        not_smelly = True



def main():
    print("This program was mainly created to strengthen my programming skills, these are the bare bones of the project and I have no clue when the project will be expanded.")

    person = input("What are you currently doing right now? (Laying on bed | On Social Media | Other)")

    if(person == "Laying on bed"):
        lay_down()
        on_sm()
        





