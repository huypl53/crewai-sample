# Debugging
## Google gemini
File at "/home/huy/miniconda3/envs/crewai/lib/python3.10/site-packages/litellm/llms/vertex_ai/gemini/vertex_and_google_ai_studio_gemini.py:L#1282"
url: 'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key='
headers: {{'Content-Type': 'application/json'}}
data: {'contents': [], 'system_instruction': {'parts': [{'text': 'Determine if the following feedback indicates that the user is satisfied or if further changes are needed. Respond with \'True\' if further changes are needed, or \'False\' if the user is satisfied. **Important** Do not include any additional commentary outside of your \'True\' or \'False\' response.\n\nFeedback: "looks good"'}]}, 'generationConfig': {'stop_sequences': ['\nObservation:']}}


## Request testing
This one gave error due to empty contents
```bash
curl -X POST \
  'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=' \
  -H 'Content-Type: application/json' \
  -d '{
        "contents": [],
        "system_instruction": {
          "parts": [
            {
              "text": "Determine if the following feedback indicates that the user is satisfied or if further changes are needed. Respond with \"True\" if further changes are needed, or \"False\" if the user is satisfied. **Important** Do not include any additional commentary outside of your \"True\" or \"False\" response.\n\nFeedback: \"looks good\""
            }
          ]
        },
        "generationConfig": {
          "stop_sequences": ["\nObservation:"]
        }
      }'
```


Provide contents to body
```bash
curl -X POST \
  'https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=' \
  -H 'Content-Type: application/json' \
  -d '{
  "contents": [
    {
      "parts": [
        {
          "text": "Determine if the following feedback indicates that the user is satisfied or if further changes are needed. Respond with \"True\" if further changes are needed, or \"False\" if the user is satisfied. **Important** Do not include any additional commentary outside of your \"True\" or \"False\" response.\n\nFeedback: \"looks good\""
        }
      ],
      "role": "model"
    }
  ],
  "systemInstruction": {
    "parts": [
      {
        "text": "Determine if the following feedback indicates that the user is satisfied or if further changes are needed. Respond with \"True\" if further changes are needed, or \"False\" if the user is satisfied. **Important** Do not include any additional commentary outside of your \"True\" or \"False\" response.\n\nFeedback: \"looks good\""
      }
    ]
  },
  "generationConfig": {
    "stop_sequences": [
      "\nObservation:"
    ]
  }
}'
```

> TODO: change body fields:
system_instruction -> systemInstruction

