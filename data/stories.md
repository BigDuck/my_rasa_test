## travel with no message
* travel_none
  - travel_form
  - form{"name": "travel_form"}
  - form{"name": null}
* affirm
  - form{"name": null}
  - action_deactivate_form
  - utter_goodbye
* deny
  - action_deactivate_form  
  - form{"name": null}
## tavel with all_time
* travel_all_time{"start_time":"明天","end_time":"后天"}
  - travel_form
  - form{"name":"travel_form"}
  - form{"name": null}
* affirm
  - form{"name": null}
  - action_deactivate_form
* deny
  - action_deactivate_form  
  - form{"name": null}


## story_greet
* greet
 - utter_greet
## story_address
* address
 - utter_address 
## story_time_entity
* time_entity
 - utter_address