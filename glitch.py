# We use the glitch.com API inorder to make everything easier for the user
# We do not store anykind of information using this API

import os, json, requests, time, sys

def create_settigs() -> None:
    open(".data/glitch_settings.json","w+").write(json.dumps({"user_is_logged_in": False, "added_project": False, "current_state": ""}))
    os.system("refresh")

def get_project():
    project_name = os.environ["PROJECT_ID"] # The ID of this Project
    project = requests.get(f'https://api.glitch.com/v1/projects/by/id?id={project_name}').json() # Info about the project (Only if not Private!)
    if len(project) > 0:
        return project[list(project.keys())[0]]
    else:
        return {}

def check_login() -> None:
    user_id = project["permissions"][0]["userId"]
    is_anon = requests.get(f'https://api.glitch.com/v1/users/by/id?id={user_id}').json()[str(user_id)]["login"] == None

    if is_anon:
        if glitch_settings["current_state"] == "waiting_for_login":
            time.sleep(1)
            sys.exit() # There are more steps needed so exit the proccess and wait until the user done them!
            # Wait a second to not spam the API is the user takes a bit longer to login...
        else:
            open("README.md","w+").write("""# Welcome 🥳\n\nEasyFN is a free Fortnite Lobbybot which allows you to see all Fortnite cosmetics.  \n\n## Steps needed  \n**Hey, you need to create yourself a Glitch.com account**  \nMobile: On the bottom left click "Sign In"  \nPC: On the top right click "Sign In"  \nYou now **need to** login using the **"Email Magic Link"** open your mailbox and wait for the Email with the code, **make sure you copy the code and paste it into the Login page you opened before**\n\n## Important\nIf you haven't already seen the [website](https://ezfn.net) make sure to check it out.  \nIf you need more help feel free to ask in our [Discord](https://discord.com/invite/qD74UYe) server.  \n\n## Installation  \n1. Remix this Project (done)  \n2. **Login to your Glitch account or make a new one (missing)**  \n3. Set to Project to private so no one can steal your account  \n4. Click on this link (complete the other steps first)  \n\n## Notice  \nYou are **not allowed** to run more than **20 Project** on **one glitch account**, so do not make more than **15 Projects** if you want that they work well  \nYou are not allowed to modify this Project in anyway if you haven't got the direct permission to do.""")
            glitch_settings["current_state"] = "waiting_for_login"
            open(".data/glitch_settings.json","w+").write(json.dumps(glitch_settings))
            os.system("refresh") # Reload the Project to make sure the user can read the new message
    else:
        #User is logged in, make sure he set the project to private
        if glitch_settings["user_is_logged_in"]:
            time.sleep(1)
            sys.exit() # There are more steps needed so exit the proccess and wait until the user done them!
        else:
            open("README.md","w+").write(f"""# Welcome 🥳\n\nEasyFN is a free Fortnite Lobbybot which allows you to see all Fortnite cosmetics.  \n\n## Steps needed  \n**Nice! you already done the first step, 2 more left!**  \nOn the top left you see "{os.environ["PROJECT_NAME"]}" click on it and then select **"Make This Project Private"** so no one can steal your bot!**  \n\n## Important\nIf you haven\'t already seen the [website](https://ezfn.net) make sure to check it out.  \nIf you need more help feel free to ask in our [Discord](https://discord.com/invite/qD74UYe) server.  \n\n## Installation  \n1. Remix this Project (done)  \n2. Login to your Glitch account or make a new one (done)  \n3. **Set to Project to private so no one can steal your account(missing)**  \n4. Click on this link (complete the other steps first)  \n\n## Notice  \nYou are **not allowed** to run more than **20 Project** on **one glitch account**, so do not make more than **15 Projects** if you want that they work well  \nYou are not allowed to modify this Project in anyway if you haven't got the direct permission to do.""")
            glitch_settings["user_is_logged_in"] = True
            open(".data/glitch_settings.json","w+").write(json.dumps(glitch_settings))
            os.system("refresh") # Reload the Project to make sure the user can read the new message

def working():
    # Yea I hate that too, but atleast it works
    if glitch_settings["added_project"] :
        return
    elif glitch_settings["current_state"] == "waiting_for_website":
        return
    else:
        if project:
            #User is logged in, make sure he set the project to private
            if glitch_settings["user_is_logged_in"]:
                time.sleep(1)
                sys.exit() # There are more steps needed so exit the proccess and wait until the user done them!
            else:
                check_login() # Make sure the user is logged in+
        else:
            # Project should be set to private and user logged in!
            if glitch_settings["user_is_logged_in"]:
                if glitch_settings["current_state"] != "waiting_for_website":
                    glitch_settings["current_state"] = "waiting_for_website"
                    open("README.md","w+").write(f"""# Welcome 🥳\n\nEasyFN is a free Fortnite Lobbybot which allows you to see all Fortnite cosmetics.   \n\n## Steps needed  \n**Last Step!**  \nClick [this](https://ezfn.net/lobbybot/create_bot?project_id={os.environ["PROJECT_ID"]}) link, you will get redirected to ezfn and this window will close.\n\n## Important\nIf you haven't already seen the [website](https://ezfn.net) make sure to check it out.  \nIf you need more help feel free to ask in our [Discord](https://discord.com/invite/qD74UYe) server.  \n\n## Installation  \n1. Remix this Project (done)  \n2. Login to your Glitch account or make a new one (done)\n3. Set to Project to private so no one can steal your account (done) \n4. Click on [this](https://ezfn.net/lobbybot/create_bot?project_id={os.environ["PROJECT_ID"]}) link (missing)\n\n## Notice  \nYou are **not allowed** to run more than **20 Project** on **one glitch account**, so do not make more than **15 Projects** if you want that they work well  \nYou are not allowed to modify this Project in anyway if you haven't got the direct permission to do.""")
                    open(".data/glitch_settings.json","w+").write(json.dumps(glitch_settings))
                    os.system("refresh")
                else:
                    time.sleep(1)
                    sys.exit() # There are more steps needed so exit the proccess and wait until the user done them!
            else:
                if glitch_settings["current_state"] == "could_not_read_data":
                    time.sleep(1)
                    sys.exit() # There are more steps needed so exit the proccess and wait until the user done them!
                else:
                    open("README.md","w+").write("""# Welcome 🥳\n\nEasyFN is a free Fortnite Lobbybot which allows you to see all Fortnite cosmetics.  \n\n## Looks like you did something wrong :/ Make sure to not set the project to private before you have dont the other steps, if you set it to private before doing the other steps just set it to public and follow the instructions""")
                    glitch_settings["current_state"] = "could_not_read_data"
                    open(".data/glitch_settings.json","w+").write(json.dumps(glitch_settings))
                    os.system("refresh") # Reload the Project to make sure the user can read the new message
       
if not os.path.exists('.data/glitch_settings.json'):
    create_settigs()
    
glitch_settings = json.loads(open(".data/glitch_settings.json").read())
if not glitch_settings["added_project"] == True:
    project = get_project()
    working()