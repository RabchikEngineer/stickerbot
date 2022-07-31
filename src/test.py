import requests


url = "https://discord.com/api/v10/applications/940295324096946237/commands"

# This is an example CHAT_INPUT or Slash Command, with a type of 1
json = {
    "name": "adas",
    "type": 1,
    "description": "Test cticker system",
    "options": [

    ]
}




# "choices": [
#                 {
#                     "name": "Dog",
#                     "value": "animal_dog"
#                 },
#                 {
#                     "name": "Cat",
#                     "value": "animal_cat"
#                 },
#                 {
#                     "name": "Penguin",
#                     "value": "animal_penguin"
#                 }]




#         {
#             "name": "only_smol",
#             "description": "Whether to show only baby animals",
#             "type": 5,
#             "required": False
#         }


# For authorization, you can use either your bot token
headers = {
    "Authorization": "Bot OTQwMjk1MzI0MDk2OTQ2MjM3.G-4cX_.Lsl4QeQtv0LQjS4ntueZKxGeDM3Ec5Cwna4SyY"
}

# or a client credentials token for your app with the applications.commands.update scope
# headers = {
#     "Authorization": "Bearer <my_credentials_token>"
# }

r = requests.post(url, headers=headers, json=json)