# Yarob-web Front end

# How to Connect to yarob

Yarob provides two main services:

* Search for a given phrase in Saved results, and lookup for similar phrases


## Lookup for a phrase
The query is like:
```
/ajaxGet?text=قال رسول الله&action=Lookup
```
Parameters are:

	* text: the input text
	* action: the action to do for the text, here the action value is "Lookup"

The Response is given like

```json
{
  "order": 0,
  "result": [
    {
      "checked": true,
      "date": "2023-07-16",
      "freq": 74,
      "inflection": "مُحَمَّدٌ: مبتدأٌمرفوعٌ وعلامةُ رفعهِ الضمةُ الظاهرةُ على آخرِهِ.<br/>رَسُولُ : خبرٌمرفوعٌ وعلامةُ رفعهِ الضمةُ الظاهرةُ على آخرِهِ.وهو مضافٌ.<br/>اللهِ: لفظُ الجلالةِ اسمٌ،مضافٌ إليهِ مجرورٌ وعلامةُ جَرِّهِ الكسرةُ الظاهرةُ على آخرِهِ .",
      "phrase": "مُحَمَّدٌ <span class=\"diff-mark\">رَسُولُ</span> <span class=\"diff-mark\">اللَّهِ</span>",
      "reference": "وب",
      "type": ""
    },
    {
      "checked": true,
      "date": "2023-07-16",
      "freq": 74,
      "inflection": "مُحَمَّدٌ: مبتدأٌمرفوعٌ وعلامةُ رفعهِ الضمةُ الظاهرةُ على آخرِهِ.<br/>رَسُولُ : خبرٌمرفوعٌ وعلامةُ رفعهِ الضمةُ الظاهرةُ على آخرِهِ.وهو مضافٌ.<br/>اللهِ: لفظُ الجلالةِ اسمٌ،مضافٌ إليهِ مجرورٌ وعلامةُ جَرِّهِ الكسرةُ الظاهرةُ على آخرِهِ .",
      "phrase": "مُحَمَّدٌ <span class=\"diff-mark\">رَسُولُ</span> <span class=\"diff-mark\">اللَّهِ</span>",
      "reference": "وب",
      "type": ""
    },
   
  ]
}
```

Response is structured as:

*  order : number of sent requests [not used now]

* result: a list of arrays for each phrase/inflection result.

* One result array contains:

  * phrase: the current phrase found in database
  * inflection: inflection of the current phrase, one word by line.
  * freq: similarity between input phrase and given result, it's between 0% to 100%
  * checked: True/False, if the given phrase inflection is checked by a human.
    * True, inflection is produced or checked by human
    * False, can be used to save users contributions or requests to be checked later.
  * date: last update date
  * type: type of phrase: can be Quran, Hadith, Poem, proverb, citation, tool word, etc.
  * reference: the given inflection's reference,  can be a book, a web site, a person.

  

  ## Inflect assist

  The query is like:

  ```
  /ajaxGet?text=قال رسول الله&action=Inflect
  ```

  Parameters are:

   * text: the input text
   * action: the action to do for the text, here the action value is "Inflect"

  The Response is given like

  ```json
  {
    "order": 0,
    "result": [
      {
        "chosen": "قَالَ",
        "inflect": "[V-1;M1H-pa-;---]{فعل ماضٍ  فعل}<br/>Verb:الماضي المعلوم:هو:y:T2G1N1",
        "link": "",
        "rule": 200,
        "semi": "قَال",
        "suggest": "قَالٌ;قَالٍ;قَالَ;قَالُ;قَالِ"
        "features": {
          "قَالٌ": [
            {
              "inflect": "",
              "tags": "مرفوع:متحرك:تنوين:::Noun:مصدر:مصدر",
              "tagscode": "---;------U;---",
              "type": "Noun:مصدر:مصدر",
              "vocalized": "قَالٌ"
            }
          ],
          "قَالٍ": [
            {
              "inflect": "",
              "tags": "مجرور:متحرك:تنوين:::Noun:مصدر:مصدر",
              "tagscode": "---;------I;---",
              "type": "Noun:مصدر:مصدر",
              "vocalized": "قَالٍ"
            }
          ],
          "قَالَ": [
            {
              "inflect": "",
              "tags": "الماضي المعلوم:هو:y::Verb",
              "tagscode": "--1;M1H-pa-;---",
              "type": "Verb",
              "vocalized": "قَالَ"
            },
            {
              "inflect": "",
              "tags": "منصوب:متحرك:ينون:::Noun:مصدر:مصدر",
              "tagscode": "---;------A;---",
              "type": "Noun:مصدر:مصدر",
              "vocalized": "قَالَ"
            }
          ]
         
        }
       
      }
    
    ]
  }
  ```

  Response is structured as:

  * order : number of sent requests [not used now]

  * result: a list of arrays for each word/inflection result.

  * One result array contains:

    * chosen: the chosen vocalized form of current word by Mishkal

    * inflect: inflection of current word, it summarize (tags code, inflection, tag list) .

      * this field is returned by Mishkal

    * link:

    * rule: the syntactic rule between current word and previous, generated by syntactic analysis.

    * semi: current word vocalization without the Last Mark تشكيل الكلمة دون علامة الإعراب

    * suggests: Alternative vocalizations of current word.

    * **Note That all previous fields are generated by Mishkal**

      * some fields are kept for legacy purpose 

    * features: an array which store inflections for alternative vocalizations, can be used to select other inflections,

      * هذا الحقل يستعمل للسماح للمستخدم باختيار تشكيل آخر للكلمة مع إعرابها

      * سيدمج هذا الخيار لاحقا مع مشكال

      * Features field contains an array of vocalized word

      * each word entry has a list of possible inflection

        ```json
         "قَالَ": [
                  {
                    "inflect": "",
                    "tags": "الماضي المعلوم:هو:y::Verb",
                    "tagscode": "--1;M1H-pa-;---",
                    "type": "Verb",
                    "vocalized": "قَالَ"
                  },
                  {
                    "inflect": "",
                    "tags": "منصوب:متحرك:ينون:::Noun:مصدر:مصدر",
                    "tagscode": "---;------A;---",
                    "type": "Noun:مصدر:مصدر",
                    "vocalized": "قَالَ"
                  }
                ]
        ```

        

    * word feature entry contains:

      * vocalized: vocalized word form
      * type: word type
      * tags: tag list in plain text
      * inflect: word form inflection
      * tagscode: encoded tag with positional codes, can be used to store tags and generate inflections

      ```
      {
          "inflect": "",
          "tags": "منصوب:متحرك:ينون:::Noun:مصدر:مصدر",
          "tagscode": "---;------A;---",
          "type": "Noun:مصدر:مصدر",
          "vocalized": "قَالَ"
      }
      ```

      