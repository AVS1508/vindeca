# Vindeca #
Vindeca is a COVID-19 Messenger Chatbot built using Python, Rasa toolkit and SpaCy NLP components, available [here](https://www.messenger.com/t/106067585064161) for testing after running the appropriate Rasa server and ngrok tunneling.

## General Implementation Details ##
The project uses Rasa's YAML-based syntax for configuring the specificities and the following table enlists the major intents (anticipated constants), entities (pre-configured variable types; variable due to synonymization) and slots (user variables).

|     Intents                    |     Entities (Synonymized)    |     Slots                       |
|--------------------------------|-------------------------------|---------------------------------|
|     nlu_fallback               |     affirmative               |     1_is_vaccinated             |
|     chitchat                   |     negative                  |     2_vaccine_brand             |
|     chitchat_options           |     happy                     |     3_num_doses                 |
|     faq                        |     sad                       |     4_past_infection            |
|     faq_options                |     usage                     |     5_current_symptoms          |
|     greet                      |     coronavirus               |     6_preexisting_conditions    |
|     goodbye                    |     assessment                |     7_travel_interstate         |
|     affirm                     |     stop                      |     requested_slot              |
|     deny                       |     information               |                                 |
|     mood_great                 |     statistics                |                                 |
|     mood_unhappy               |     guidance                  |                                 |
|     usage_cases                |     symptoms                  |                                 |
|     coronavirus_assessment     |     healthcare                |                                 |
|     stop_form                  |     quarantine                |                                 |
|     coronavirus_information    |     vaccine                   |                                 |
|     coronavirus_statistics     |                               |                                 |
|     coronavirus_guidance       |                               |                                 |
|     coronavirus_symptoms       |                               |                                 |
|     coronavirus_healthcare     |                               |                                 |
|     coronavirus_vaccine        |                               |                                 |

The project utilized Rasa for building the NLU data pipeline as well as the NLG responses section, and Rasa X was used to generate additional stories using the pre-configured rules and stories, i.e., an amalgamation of rule-based system and learning-based system to create a hybrid system of text classification by the Health Bot. Also, spaCy’s Tokenizer and Featurizer were used in congruence with spaCy’s NLP model, instead of typical Whitespace Tokenizer and along with usual RegexFeaturizer. The reason behind this decision was to subscribe to spaCy ecosystem which would be more conducive for non-European language structures, thus enabling the chatbot to be able to even understand Google-translated queries from Hindi, Bengali, Marathi, Punjabi, and other Indian languages. This makes the chatbot more inclusive of non-native English speakers and even people who are not comfortable with English at all.

## Feature Set Details ##

### COVID-19 Self Assessment ###

This self-assessment feature allows the user to estimate their risk of exposure to COVID-19 and the consequent issues, using just a simple questionnaire that can be completed in less than a minute. It is modeled based on Aarogya Setu’s feature of the same name. It has a total variation of 6 different outcomes, primarily based on the vaccination status and adverse factors (stressors). Here are two different outcomes that are diametrically opposite.
![image](https://user-images.githubusercontent.com/20084950/216230383-8ec5cfda-da47-46f8-b9f5-456206d87dab.png)

### COVID-19 Information ###

This information panel has a total of 5 different avenues, namely COVID-19 statistics, guidance, symptoms, healthcare, and vaccines. For examples, the below depicts the COVID-19 statistics:

<img width="427" alt="image" src="https://user-images.githubusercontent.com/20084950/216230760-ffd8d726-bf08-40c2-b972-2e4517868fe3.png">

Following this, we have the COVID-19 guidelines response:

<img width="427" alt="image" src="https://user-images.githubusercontent.com/20084950/216230971-8cb2718e-862c-4f8f-919f-6f3b731a9abe.png">

Then, we have the option of viewing a list of COVID-19 symptoms:

<img width="427" alt="image" src="https://user-images.githubusercontent.com/20084950/216230997-41e904a4-4579-471c-807d-b817d7eb28a7.png">

We also have the ability to search for COVID-19 healthcare options:

<img width="427" alt="image" src="https://user-images.githubusercontent.com/20084950/216231148-ab220d23-ba21-47b4-83e4-0d556080976f.png">

Finally, there is also the option to look for vaccination slots for COVID-19:

<img width="427" alt="image" src="https://user-images.githubusercontent.com/20084950/216231182-44276528-d1c4-4ec8-b83f-a6614a4c628c.png">

### Chitchat ###

The bot has the ability to make small talk such as responding with its name, and guessing the weather based on a random draw.

<img width="427" alt="image" src="https://user-images.githubusercontent.com/20084950/216231278-3d409bbf-1eb7-4cb1-9652-f77ca087702a.png">

<img width="427" alt="image" src="https://user-images.githubusercontent.com/20084950/216231284-7fc2b2d1-38e0-4b43-985d-8bcac8c19d91.png">

### FAQs ###

The bot also manages to answer frequently asked questions such as the definition of COVID-19 and the medium of contagion for the same.

<img width="427" alt="image" src="https://user-images.githubusercontent.com/20084950/216231327-4e5a088d-e49b-46c0-8ece-37e4c1eba85d.png">

<img width="427" alt="image" src="https://user-images.githubusercontent.com/20084950/216231341-0a3b9c21-ea24-4e86-86ab-92d156861ba8.png">

### Cheering Up Unhappy Users ###

There is a feature of reciting a joke in order to lighten the mood, in case the user feels sad/unhappy during the course of conversation.

<img width="427" alt="image" src="https://user-images.githubusercontent.com/20084950/216231381-119a15dc-d65b-44d3-9f11-00e15b6b763e.png">

### Handling Happy Users ###

In case the user feels happy in general, the Health Bot is receptive to it and conveys its happiness for the same.

<img width="427" alt="image" src="https://user-images.githubusercontent.com/20084950/216231409-f6d51bcf-4a29-48e4-ac65-8e9f9c4406d3.png">

## Minor Feature Implementations ##

### Rasa Chitchat/FAQs ###

The Health Bot uses Rasa’s in-built functionality for handling small talk and frequently asked questions by avoiding excessive intents in favor of a group of intents classed under “chitchat” or “faq” intents. This also allows for the user to break the flow of the current operation at any time and ask time-sensitive queries.

### Form Validation ###

There is also custom action form validation for the COVID-19 Self-Assessment feature, so that the Health Bot doesn’t make conclusions with incorrectly formatted inputs, and reiterates its need for correctly specified details.

### Form Deactivation and Unhappy Path ###

There is also a custom action for handling form deactivation (ensuring that the form doesn’t keep asking for slots) which also ensures that the form data is cleaned post current assessment is explained. The user may also break the execution of a form (indicative of an unhappy conversation path) apart from the typical Chitchat/FAQs, through expressing a desire of stopping the form questions using phrases with some specific keywords such as “stop”, “pause”, “halt”, et cetera. 

### Image Inclusion ###

There are also images included with the responses for the COVID-19 information section, which depicts the previously mentioned links’ websites. It helps to visualize the look of a website as well as highlight the fact that a link has been shared, which may be perused by the user at their discretion in contrast to an automatic redirection to the relevant external website.There are also images included with the responses for the COVID-19 information section, which depicts the previously mentioned links’ websites. It helps to visualize the look of a website as well as highlight the fact that a link has been shared, which may be perused by the user at their discretion in contrast to an automatic redirection to the relevant external website.

### Facebook Messenger Quick Replies ###

The Health Bot also utilizes Facebook-specific quick replies that enables users to select from a list of potential options for a query, which also makes it more accessible to people who may not be acquainted with the intricacies of common English. The quick replies also reduces the need for long user utterances to be examined by the NLU component, as they already carry a payload (with intent specified).

### Rasa/Messenger Buttons ###

The Health Bot utilizes Rasa buttons on Messenger that enables users to choose between “Yes”/“No” options with greater ease and more specificity as payloads are used again to clarify the intents (affirmative/negative) respectively. Buttons also add another UI tangent for the user to have a better UX, and thus enables the chatbot to have a hybridized system of menu-based chatbot as well as machine-learning-based chatbot.

### Synonymization & spaCy ###

The Health Bot also uses a variety of entities that utilize synonymization in order to allow for greate variations of user utterances being correctly identified/understood, which makes the chatbot more receptive towards various common English proficiencies. Using the spaCy model along with it, builds a better confluence of intents and entities, resolving most queries with great ease. The NLU fallback is also configured to simply not respond in cases where there are more than one significant intent identified.
