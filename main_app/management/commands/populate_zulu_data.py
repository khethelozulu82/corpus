from django.core.management.base import BaseCommand
from main_app.models import ZuluWord, WordPair
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Populates the database with sample isiZulu words and phrases'
    
    def handle(self, *args, **options):
        # Sample isiZulu words with cultural context
        zulu_words = [
    {
        "zulu_word": "Sawubona",
        "english_translation": "Hello",
        "swati_translation": "Sawubona",
        "pronunciation_guide": "sah-woo-BOH-nah",
        "part_of_speech": "greeting",
        "cultural_context": "A common greeting meaning 'I see you'. It acknowledges the presence and humanity of the other person.",
        "example_sentence_zulu": "Sawubona, unjani?",
        "example_sentence_english": "Hello, how are you?",
        "example_sentence_swati": "Sawubona, unjani?"
    },
    {
        "zulu_word": "Hamba kahle",
        "english_translation": "Go well",
        "swati_translation": "Hamba kahle",
        "pronunciation_guide": "HAHM-bah KAH-shleh",
        "part_of_speech": "farewell",
        "cultural_context": "A common farewell wishing someone a safe journey. The response is 'Sala kahle' (Stay well).",
        "example_sentence_zulu": "Hamba kahle, ngizokubona ekamelweni.",
        "example_sentence_english": "Go well, I will see you at home.",
        "example_sentence_swati": "Hamba kahle, ngitokubona ekhaya."
    },
    {
        "zulu_word": "Ubuntu",
        "english_translation": "Humanity",
        "swati_translation": "Buntfu",
        "pronunciation_guide": "oo-BOON-too",
        "part_of_speech": "noun",
        "cultural_context": "A philosophy emphasizing community, sharing, and interconnectedness. Often translated as 'I am because we are'.",
        "example_sentence_zulu": "Ubuntu buyindlela yokuphila emphakathini.",
        "example_sentence_english": "Ubuntu is a way of living in community.",
        "example_sentence_swati": "Buntfu buyindlela yekuphila emiphakatsini."
    },
    {
        "zulu_word": "Imbeleko",
        "english_translation": "Traditional baby carrier",
        "swati_translation": "Imbeleko",
        "pronunciation_guide": "im-beh-LEH-koh",
        "part_of_speech": "noun",
        "cultural_context": "A ceremony where a newborn is introduced to the ancestors. Also refers to the cloth used to carry babies.",
        "example_sentence_zulu": "Umntwana uphethwe ngembeleko esegazini.",
        "example_sentence_english": "The baby is carried with a cloth on the back.",
        "example_sentence_swati": "Umntfwana utsetfwelwa ngembeleko emhlane."
    },
    {
        "zulu_word": "Indaba",
        "english_translation": "Meeting or conference",
        "swati_translation": "Indzaba",
        "pronunciation_guide": "in-DAH-bah",
        "part_of_speech": "noun",
        "cultural_context": "A gathering to discuss important matters. Traditionally, it was a meeting of elders to make community decisions.",
        "example_sentence_zulu": "Sizoba neNdaba enkulu ngesonto elizayo.",
        "example_sentence_english": "We will have a big meeting next week.",
        "example_sentence_swati": "Sitawuba nendzaba lenkhulu ngesonto lelitako."
    },
    {
        "zulu_word": "Inyoni",
        "english_translation": "Bird",
        "swati_translation": "Inyoni",
        "pronunciation_guide": "in-YOH-nee",
        "part_of_speech": "noun",
        "cultural_context": "Birds often feature in Zulu folklore and are sometimes considered messengers or omens.",
        "example_sentence_zulu": "Inyoni ihlabela emini.",
        "example_sentence_english": "The bird sings during the day.",
        "example_sentence_swati": "Inyoni icula emini."
    },
    {
        "zulu_word": "Isidwaba",
        "english_translation": "Traditional skirt",
        "swati_translation": "Sidvaba",
        "pronunciation_guide": "is-ee-DWAH-bah",
        "part_of_speech": "noun",
        "cultural_context": "A leather skirt worn by married Zulu women, often decorated with beads.",
        "example_sentence_zulu": "Isidwaba sibekwa ngamabala amahle.",
        "example_sentence_english": "The traditional skirt is decorated with beautiful patterns.",
        "example_sentence_swati": "Sidvaba sifakwa ngemabala lamahle."
    },
    {
        "zulu_word": "Ukubonga",
        "english_translation": "To thank",
        "swati_translation": "Kubonga",
        "pronunciation_guide": "oo-koo-BOHN-gah",
        "part_of_speech": "verb",
        "cultural_context": "Expressing gratitude is important in Zulu culture, often extending beyond people to include ancestors.",
        "example_sentence_zulu": "Ngizokubonga ngosizo lwakho.",
        "example_sentence_english": "I will thank you for your help.",
        "example_sentence_swati": "Ngitawukubonga ngesita sakho."
    },
    {
        "zulu_word": "Inhliziyo",
        "english_translation": "Heart",
        "swati_translation": "Inhlitiyo",
        "pronunciation_guide": "in-hlee-ZEE-yoh",
        "part_of_speech": "noun",
        "cultural_context": "In Zulu culture, the heart represents emotions, courage, and the center of one's being.",
        "example_sentence_zulu": "Inhliziyo yami ibuhlungu.",
        "example_sentence_english": "My heart is sore (I am sad).",
        "example_sentence_swati": "Inhlitiyo yami ibuhlungu."
    },
    {
        "zulu_word": "Ukudla",
        "english_translation": "Food",
        "swati_translation": "Kudla",
        "pronunciation_guide": "oo-KOOD-lah",
        "part_of_speech": "noun",
        "cultural_context": "Sharing food is an important part of Zulu culture and hospitality.",
        "example_sentence_zulu": "Sidla ukudla okumnandi.",
        "example_sentence_english": "We eat delicious food.",
        "example_sentence_swati": "Sidla kudla lokumnandi."
    },
    {
        "zulu_word": "Umuzi",
        "english_translation": "Homestead",
        "swati_translation": "Umuti",
        "pronunciation_guide": "oo-MOO-zee",
        "part_of_speech": "noun",
        "cultural_context": "A traditional Zulu homestead consists of several huts arranged in a circle.",
        "example_sentence_zulu": "Umuzi wethu mkhulu.",
        "example_sentence_english": "Our homestead is big.",
        "example_sentence_swati": "Umuti wetfu mukhulu."
    },
    {
        "zulu_word": "Inkomo",
        "english_translation": "Cow",
        "swati_translation": "Inkhomo",
        "pronunciation_guide": "in-KOH-moh",
        "part_of_speech": "noun",
        "cultural_context": "Cows are highly valued in Zulu culture, representing wealth and status.",
        "example_sentence_zulu": "Inkomo idla utshani.",
        "example_sentence_english": "The cow eats grass.",
        "example_sentence_swati": "Inkhomo idla lucwati."
    },
    {
        "zulu_word": "Ukucula",
        "english_translation": "To sing",
        "swati_translation": "Kucula",
        "pronunciation_guide": "oo-koo-CHOO-lah",
        "part_of_speech": "verb",
        "cultural_context": "Singing is an integral part of Zulu culture, used in ceremonies, celebrations, and storytelling.",
        "example_sentence_zulu": "Abantu bacula ingoma.",
        "example_sentence_english": "The people are singing a song.",
        "example_sentence_swati": "Bantfu bacula ingoma."
    },
    {
        "zulu_word": "Isigqoko",
        "english_translation": "Hat",
        "swati_translation": "Sigqoko",
        "pronunciation_guide": "is-ee-GOH-koh",
        "part_of_speech": "noun",
        "cultural_context": "Traditional Zulu hats are often beautifully beaded and signify cultural identity.",
        "example_sentence_zulu": "Isigqoko sami sihle.",
        "example_sentence_english": "My hat is beautiful.",
        "example_sentence_swati": "Sigqoko sami sihle."
    },
    {
        "zulu_word": "Ukwelapha",
        "english_translation": "To heal",
        "swati_translation": "Kwelapha",
        "pronunciation_guide": "oo-kweh-LAH-pah",
        "part_of_speech": "verb",
        "cultural_context": "Traditional healing practices are respected in Zulu culture, often involving herbal medicine and spiritual guidance.",
        "example_sentence_zulu": "Inyanga iyelapha abagulayo.",
        "example_sentence_english": "The traditional healer heals the sick.",
        "example_sentence_swati": "Inyanga iyelapha labagula."
    },
    {
        "zulu_word": "Imbizo",
        "english_translation": "Gathering",
        "swati_translation": "Imbito",
        "pronunciation_guide": "im-BEE-zoh",
        "part_of_speech": "noun",
        "cultural_context": "A community gathering for discussion, decision-making, or celebration.",
        "example_sentence_zulu": "Sinenmbizo yomphakathi.",
        "example_sentence_english": "We have a community gathering.",
        "example_sentence_swati": "Sinenbito yemphakatsi."
    },
    {
        "zulu_word": "Ukusiza",
        "english_translation": "To help",
        "swati_translation": "Kusita",
        "pronunciation_guide": "oo-koo-SEE-zah",
        "part_of_speech": "verb",
        "cultural_context": "Community support and helping others is a core value in Zulu culture.",
        "example_sentence_zulu": "Ngizokusiza wena.",
        "example_sentence_english": "I will help you.",
        "example_sentence_swati": "Ngitokusita wena."
    },
    {
        "zulu_word": "Isibongo",
        "english_translation": "Clan name",
        "swati_translation": "Sibongo",
        "pronunciation_guide": "is-ee-BOHN-goh",
        "part_of_speech": "noun",
        "cultural_context": "Clan names are important in Zulu culture, connecting individuals to their ancestry and heritage.",
        "example_sentence_zulu": "Isibongo sakho siyini?",
        "example_sentence_english": "What is your clan name?",
        "example_sentence_swati": "Sibongo sakho siyini?"
    },
    {
        "zulu_word": "Ukukhulekela",
        "english_translation": "To pray for",
        "swati_translation": "Kukhulekela",
        "pronunciation_guide": "oo-koo-khoo-leh-KEH-lah",
        "part_of_speech": "verb",
        "cultural_context": "Prayer and connection with ancestors is an important spiritual practice.",
        "example_sentence_zulu": "Ngiyakukhulekela wena.",
        "example_sentence_english": "I am praying for you.",
        "example_sentence_swati": "Ngiyakukhulekela wena."
    },
    {
        "zulu_word": "Inyanga",
        "english_translation": "Traditional healer",
        "swati_translation": "Inyanga",
        "pronunciation_guide": "in-YAHN-gah",
        "part_of_speech": "noun",
        "cultural_context": "Traditional healers are respected figures who use herbs, divination, and spiritual guidance.",
        "example_sentence_zulu": "Inyanga iyelapha ngemithi.",
        "example_sentence_english": "The traditional healer heals with herbs.",
        "example_sentence_swati": "Inyanga iyelapha ngemitsi."
    },
    {
        "zulu_word": "Ukwelusa",
        "english_translation": "To herd",
        "swati_translation": "Kwelusa",
        "pronunciation_guide": "oo-kweh-LOO-sah",
        "part_of_speech": "verb",
        "cultural_context": "Cattle herding has traditionally been an important role, especially for young men.",
        "example_sentence_zulu": "Abafana belusa izinkomo.",
        "example_sentence_english": "The boys are herding cattle.",
        "example_sentence_swati": "Bafana belusa tinkhomo."
    },
    {
        "zulu_word": "Isicathamiya",
        "english_translation": "A cappella music",
        "swati_translation": "Sicathamiya",
        "pronunciation_guide": "is-ee-cah-tah-MEE-yah",
        "part_of_speech": "noun",
        "cultural_context": "A style of unaccompanied singing that originated among Zulu migrant workers.",
        "example_sentence_zulu": "Izingoma zesicathamiya zithokozisa.",
        "example_sentence_english": "Isicathamiya songs are enjoyable.",
        "example_sentence_swati": "Tingoma tesicathamiya tiyajabulisa."
    },
    {
        "zulu_word": "Ukusindisa",
        "english_translation": "To save",
        "swati_translation": "Kusindzisa",
        "pronunciation_guide": "oo-koo-sin-DEE-sah",
        "part_of_speech": "verb",
        "cultural_context": "The concept of saving or rescuing has both practical and spiritual meanings.",
        "example_sentence_zulu": "Ungisindise ebulaleni.",
        "example_sentence_english": "Save me from danger.",
        "example_sentence_swati": "Ungisindzise engozini."
    },
    {
        "zulu_word": "Sawubona",
        "english_translation": "Hello",
        "swati_translation": "Sawubona",
        "pronunciation_guide": "sah-woo-BOH-nah",
        "part_of_speech": "greeting",
        "cultural_context": "Standard greeting meaning 'I see you' - acknowledges the presence of another person.",
        "example_sentence_zulu": "Sawubona, unjani namhlanje?",
        "example_sentence_english": "Hello, how are you today?",
        "example_sentence_swati": "Sawubona, unjani namuhla?"
    },
    {
        "zulu_word": "Hamba kahle",
        "english_translation": "Go well",
        "swati_translation": "Hamba kahle",
        "pronunciation_guide": "HAHM-bah KAH-shleh",
        "part_of_speech": "farewell",
        "cultural_context": "Common farewell wishing someone a safe journey.",
        "example_sentence_zulu": "Hamba kahle, ubuye ngokuthula.",
        "example_sentence_english": "Go well, return in peace.",
        "example_sentence_swati": "Hamba kahle, ubuye ngekuthula."
    },
    {
        "zulu_word": "Yebo",
        "english_translation": "Yes",
        "swati_translation": "Yebo",
        "pronunciation_guide": "YEH-boh",
        "part_of_speech": "interjection",
        "cultural_context": "Standard affirmative response, also used to show respect when addressing elders.",
        "example_sentence_zulu": "Yebo, ngiyaqonda.",
        "example_sentence_english": "Yes, I understand.",
        "example_sentence_swati": "Yebo, ngiyacondza."
    },
    {
        "zulu_word": "Cha",
        "english_translation": "No",
        "swati_translation": "Cha",
        "pronunciation_guide": "CHAH",
        "part_of_speech": "interjection",
        "cultural_context": "Standard negative response.",
        "example_sentence_zulu": "Cha, angikufuni lokho.",
        "example_sentence_english": "No, I don't want that.",
        "example_sentence_swati": "Cha, angikufuni loko."
    },
    {
        "zulu_word": "Ngiyabonga",
        "english_translation": "Thank you",
        "swati_translation": "Ngiyabonga",
        "pronunciation_guide": "ngee-yah-BOHN-gah",
        "part_of_speech": "expression",
        "cultural_context": "Expression of gratitude, important in social interactions.",
        "example_sentence_zulu": "Ngiyabonga ngosizo lwakho.",
        "example_sentence_english": "Thank you for your help.",
        "example_sentence_swati": "Ngiyabonga ngesita sakho."
    },
    {
        "zulu_word": "Uxolo",
        "english_translation": "Sorry/Excuse me",
        "swati_translation": "Xolisa",
        "pronunciation_guide": "oo-KHOH-loh",
        "part_of_speech": "expression",
        "cultural_context": "Used to apologize or get someone's attention politely.",
        "example_sentence_zulu": "Uxolo, ngicela ungisize.",
        "example_sentence_english": "Excuse me, please help me.",
        "example_sentence_swati": "Xolisa, ngicela ungisite."
    },
    {
        "zulu_word": "Kulungile",
        "english_translation": "Okay",
        "swati_translation": "Kulungile",
        "pronunciation_guide": "koo-loon-GEE-leh",
        "part_of_speech": "interjection",
        "cultural_context": "Used to express agreement or acceptance.",
        "example_sentence_zulu": "Kulungile, ngizokwenza kanjalo.",
        "example_sentence_english": "Okay, I will do it like that.",
        "example_sentence_swati": "Kulungile, ngitokwenta kanjalo."
    },
    {
        "zulu_word": "Unjani?",
        "english_translation": "How are you?",
        "swati_translation": "Unjani?",
        "pronunciation_guide": "oon-JAH-nee",
        "part_of_speech": "phrase",
        "cultural_context": "Common greeting asking about someone's well-being.",
        "example_sentence_zulu": "Sawubona, unjani?",
        "example_sentence_english": "Hello, how are you?",
        "example_sentence_swati": "Sawubona, unjani?"
    },
    {
        "zulu_word": "Ngisaphila",
        "english_translation": "I am still alive",
        "swati_translation": "Ngisaphila",
        "pronunciation_guide": "ngee-sah-PEE-lah",
        "part_of_speech": "response",
        "cultural_context": "Common response to 'Unjani?' meaning you're doing fine.",
        "example_sentence_zulu": "Ngiyaphila, ngisaphila.",
        "example_sentence_english": "I'm fine, I'm still alive.",
        "example_sentence_swati": "Ngiyaphila, ngisaphila."
    },
    {
        "zulu_word": "Sala kahle",
        "english_translation": "Stay well",
        "swati_translation": "Sala kahle",
        "pronunciation_guide": "SAH-lah KAH-shleh",
        "part_of_speech": "farewell",
        "cultural_context": "Response to 'Hamba kahle' - wishing someone to remain well.",
        "example_sentence_zulu": "Sala kahle, ngizobuya maduzane.",
        "example_sentence_english": "Stay well, I will return soon.",
        "example_sentence_swati": "Sala kahle, ngitobuya masinyane."
    },
    {
        "zulu_word": "Umama",
        "english_translation": "Mother",
        "swati_translation": "Make",
        "pronunciation_guide": "oo-MAH-mah",
        "part_of_speech": "noun",
        "cultural_context": "Term for mother, shows respect for the maternal figure in the family.",
        "example_sentence_zulu": "Umama upheke ukudla okumnandi.",
        "example_sentence_english": "Mother cooked delicious food.",
        "example_sentence_swati": "Make upheke kudla lokumnandi."
    },
    {
        "zulu_word": "Ubaba",
        "english_translation": "Father",
        "swati_translation": "Babe",
        "pronunciation_guide": "oo-BAH-bah",
        "part_of_speech": "noun",
        "cultural_context": "Term for father, the patriarchal figure in the family structure.",
        "example_sentence_zulu": "Ubaba usebenza emsebenzini.",
        "example_sentence_english": "Father works at his job.",
        "example_sentence_swati": "Babe usebenta emsebentini."
    },
    {
        "zulu_word": "Umfana",
        "english_translation": "Boy",
        "swati_translation": "Umfana",
        "pronunciation_guide": "oom-FAH-nah",
        "part_of_speech": "noun",
        "cultural_context": "Refers to a young male, often before initiation into adulthood.",
        "example_sentence_zulu": "Umfana udlala ngaphandle.",
        "example_sentence_english": "The boy is playing outside.",
        "example_sentence_swati": "Umfana udlala ngaphandle."
    },
    {
        "zulu_word": "Intombi",
        "english_translation": "Girl",
        "swati_translation": "Intfombi",
        "pronunciation_guide": "in-TOHM-bee",
        "part_of_speech": "noun",
        "cultural_context": "Refers to a young female, before marriage or adulthood.",
        "example_sentence_zulu": "Intombi icula ingoma.",
        "example_sentence_english": "The girl is singing a song.",
        "example_sentence_swati": "Intfombi icula ingoma."
    },
    {
        "zulu_word": "Umngane",
        "english_translation": "Friend",
        "swati_translation": "Umngani",
        "pronunciation_guide": "oom-NGAH-neh",
        "part_of_speech": "noun",
        "cultural_context": "Close companion, friendship is highly valued in Zulu culture.",
        "example_sentence_zulu": "Umngane wami ufika ekuseni.",
        "example_sentence_english": "My friend arrives in the morning.",
        "example_sentence_swati": "Umngani wami ufika ekuseni."
    },
    {
        "zulu_word": "Umndeni",
        "english_translation": "Family",
        "swati_translation": "Umndeni",
        "pronunciation_guide": "oom-NDEH-nee",
        "part_of_speech": "noun",
        "cultural_context": "The extended family unit, which is central to Zulu social structure.",
        "example_sentence_zulu": "Umndeni wami muhle.",
        "example_sentence_english": "My family is beautiful.",
        "example_sentence_swati": "Umndeni wami muhle."
    },
    {
        "zulu_word": "Udade",
        "english_translation": "Sister",
        "swati_translation": "Sisi",
        "pronunciation_guide": "oo-DAH-deh",
        "part_of_speech": "noun",
        "cultural_context": "Sister, can refer to biological sister or close female friend.",
        "example_sentence_zulu": "Udade wami ufundisa esikoleni.",
        "example_sentence_english": "My sister teaches at school.",
        "example_sentence_swati": "Sisi wami ufundzisa esikoleni."
    },
    {
        "zulu_word": "Umfowethu",
        "english_translation": "My brother",
        "swati_translation": "Mtfowetfu",
        "pronunciation_guide": "oom-foh-WEH-too",
        "part_of_speech": "noun",
        "cultural_context": "My brother, shows possession and close familial relationship.",
        "example_sentence_zulu": "Umfowethu usebenza edolobheni.",
        "example_sentence_english": "My brother works in the city.",
        "example_sentence_swati": "Mtfowetfu usebenta edolobheni."
    },
    {
        "zulu_word": "Ugogo",
        "english_translation": "Grandmother",
        "swati_translation": "Gogo",
        "pronunciation_guide": "oo-GOH-goh",
        "part_of_speech": "noun",
        "cultural_context": "Grandmother, respected elder who often preserves cultural knowledge.",
        "example_sentence_zulu": "Ugogo uxoxa indaba.",
        "example_sentence_english": "Grandmother is telling a story.",
        "example_sentence_swati": "Gogo uxoxa indzaba."
    },
    {
        "zulu_word": "Umkhulu",
        "english_translation": "Grandfather",
        "swati_translation": "Mkhulu",
        "pronunciation_guide": "oom-KHOO-loo",
        "part_of_speech": "noun",
        "cultural_context": "Grandfather, respected elder and family patriarch.",
        "example_sentence_zulu": "Umkhulu ufunda incwadi.",
        "example_sentence_english": "Grandfather is reading a book.",
        "example_sentence_swati": "Mkhulu ufundza incwadzi."
    },
    {
        "zulu_word": "Kunye",
        "english_translation": "One",
        "swati_translation": "Kunye",
        "pronunciation_guide": "KOO-nyeh",
        "part_of_speech": "number",
        "cultural_context": "The number one, used in counting and cultural contexts.",
        "example_sentence_zulu": "Nginenkomo eyodwa.",
        "example_sentence_english": "I have one cow.",
        "example_sentence_swati": "Nginemkhomo yinye."
    },
    {
        "zulu_word": "Kubili",
        "english_translation": "Two",
        "swati_translation": "Kubili",
        "pronunciation_guide": "koo-BEE-lee",
        "part_of_speech": "number",
        "cultural_context": "The number two, important in paired concepts and traditions.",
        "example_sentence_zulu": "Nginabantwana ababili.",
        "example_sentence_english": "I have two children.",
        "example_sentence_swati": "Nginabantfwana babili."
    },
    {
        "zulu_word": "Kuthathu",
        "english_translation": "Three",
        "swati_translation": "Kutsatfu",
        "pronunciation_guide": "koo-THAH-too",
        "part_of_speech": "number",
        "cultural_context": "The number three, appears in various cultural expressions.",
        "example_sentence_zulu": "Kunezinkomo ezintathu.",
        "example_sentence_english": "There are three cows.",
        "example_sentence_swati": "Kunetinkhomo tetatsatfu."
    },
    {
        "zulu_word": "Kune",
        "english_translation": "Four",
        "swati_translation": "Kune",
        "pronunciation_guide": "KOO-neh",
        "part_of_speech": "number",
        "cultural_context": "The number four, used in counting and traditional practices.",
        "example_sentence_zulu": "Sinezimoto ezine.",
        "example_sentence_english": "We have four cars.",
        "example_sentence_swati": "Sinetimoto letine."
    },
    {
        "zulu_word": "Kuhlanu",
        "english_translation": "Five",
        "swati_translation": "Kuhlanu",
        "pronunciation_guide": "koo-HLAH-noo",
        "part_of_speech": "number",
        "cultural_context": "The number five, significant in various cultural contexts.",
        "example_sentence_zulu": "Ngizohamba ezinsukwini ezinhlanu.",
        "example_sentence_english": "I will go in five days.",
        "example_sentence_swati": "Ngitawuhamba etinsukwini tetinhlanu."
    },
    {
        "zulu_word": "Isithupha",
        "english_translation": "Six",
        "swati_translation": "Sitfupha",
        "pronunciation_guide": "is-ee-THOO-pah",
        "part_of_speech": "number",
        "cultural_context": "The number six.",
        "example_sentence_zulu": "Nginamaminithi ayisithupha.",
        "example_sentence_english": "I have six minutes.",
        "example_sentence_swati": "Nginemaminitsi lasitfupha."
    },
    {
        "zulu_word": "Isikhombisa",
        "english_translation": "Seven",
        "swati_translation": "Sikhombisa",
        "pronunciation_guide": "is-ee-khom-BEE-sah",
        "part_of_speech": "number",
        "cultural_context": "The number seven.",
        "example_sentence_zulu": "Kunezinyoni eziyisikhombisa.",
        "example_sentence_english": "There are seven birds.",
        "example_sentence_swati": "Kunetinyoni letisikhombisa."
    },
    {
        "zulu_word": "Isishiyagalombili",
        "english_translation": "Eight",
        "swati_translation": "Sishiyagalombili",
        "pronunciation_guide": "is-ee-shee-yah-gah-lom-BEE-lee",
        "part_of_speech": "number",
        "cultural_context": "The number eight, literally 'remaining two from ten'.",
        "example_sentence_zulu": "Sinezincwadi eziyisishiyagalombili.",
        "example_sentence_english": "We have eight books.",
        "example_sentence_swati": "Sinetincwadzi letishiyagalombili."
    },
    {
        "zulu_word": "Isishiyagalolunye",
        "english_translation": "Nine",
        "swati_translation": "Sishiyagalolunye",
        "pronunciation_guide": "is-ee-shee-yah-gah-loh-LOO-nyeh",
        "part_of_speech": "number",
        "cultural_context": "The number nine, literally 'remaining one from ten'.",
        "example_sentence_zulu": "Kunamaphepha ayisishiyagalolunye.",
        "example_sentence_english": "There are nine papers.",
        "example_sentence_swati": "Kunamaphepha lashiyagalolunye."
    },
    {
        "zulu_word": "Ishumi",
        "english_translation": "Ten",
        "swati_translation": "Lishumi",
        "pronunciation_guide": "ee-SHOO-mee",
        "part_of_speech": "number",
        "cultural_context": "The number ten, a complete set in many cultural contexts.",
        "example_sentence_zulu": "Nginamadola ayishumi.",
        "example_sentence_english": "I have ten dollars.",
        "example_sentence_swati": "Nginemadola lelishumi."
    },
    {
        "zulu_word": "Inja",
        "english_translation": "Dog",
        "swati_translation": "Inja",
        "pronunciation_guide": "IN-jah",
        "part_of_speech": "noun",
        "cultural_context": "Dogs are kept for hunting and protection in traditional homesteads.",
        "example_sentence_zulu": "Inja ilindela umuzi.",
        "example_sentence_english": "The dog guards the homestead.",
        "example_sentence_swati": "Inja ilindzela umuti."
    },
    {
        "zulu_word": "Ikati",
        "english_translation": "Cat",
        "swati_translation": "Likati",
        "pronunciation_guide": "ee-KAH-tee",
        "part_of_speech": "noun",
        "cultural_context": "Cats are kept for controlling rodents in traditional homes.",
        "example_sentence_zulu": "Ikati lidla igundane.",
        "example_sentence_english": "The cat eats the mouse.",
        "example_sentence_swati": "Likati lidla ligundvwane."
    },
    {
        "zulu_word": "Ihashi",
        "english_translation": "Horse",
        "swati_translation": "Lihhashi",
        "pronunciation_guide": "ee-HAH-shee",
        "part_of_speech": "noun",
        "cultural_context": "Horses were historically important for transportation and warfare.",
        "example_sentence_zulu": "Ihashi libaleka ngokushesha.",
        "example_sentence_english": "The horse runs fast.",
        "example_sentence_swati": "Lihhashi ligijima ngekukhawuleta."
    },
    {
        "zulu_word": "Umbila",
        "english_translation": "Maize",
        "swati_translation": "Ummbila",
        "pronunciation_guide": "oom-BEE-lah",
        "part_of_speech": "noun",
        "cultural_context": "Maize is the staple food, used to make pap/porridge.",
        "example_sentence_zulu": "Umbila uyavuna.",
        "example_sentence_english": "The maize is ready for harvest.",
        "example_sentence_swati": "Ummbila uyavuna."
    },
    {
        "zulu_word": "Amazambane",
        "english_translation": "Potatoes",
        "swati_translation": "Ematamatisi",
        "pronunciation_guide": "ah-mah-zahm-BAH-neh",
        "part_of_speech": "noun",
        "cultural_context": "Potatoes are a common vegetable in traditional meals.",
        "example_sentence_zulu": "Amazambane aphekile.",
        "example_sentence_english": "The potatoes are cooked.",
        "example_sentence_swati": "Ematamatisi aphekiwe."
    },
    {
        "zulu_word": "Intaba",
        "english_translation": "Mountain",
        "swati_translation": "Intaba",
        "pronunciation_guide": "in-TAH-bah",
        "part_of_speech": "noun",
        "cultural_context": "Mountains often have spiritual significance in Zulu culture.",
        "example_sentence_zulu": "Intaba inkulu.",
        "example_sentence_english": "The mountain is big.",
        "example_sentence_swati": "Intaba inkhulu."
    },
    {
        "zulu_word": "Umfula",
        "english_translation": "River",
        "swati_translation": "Umfula",
        "pronunciation_guide": "oom-FOO-lah",
        "part_of_speech": "noun",
        "cultural_context": "Rivers are important water sources and often feature in folklore.",
        "example_sentence_zulu": "Umfula ugeleza ngokuthula.",
        "example_sentence_english": "The river flows peacefully.",
        "example_sentence_swati": "Umfula ugeleza ngekuthula."
    },
    {
        "zulu_word": "Hamba",
        "english_translation": "Go",
        "swati_translation": "Hamba",
        "pronunciation_guide": "HAHM-bah",
        "part_of_speech": "verb",
        "cultural_context": "Basic verb for movement, used in many expressions and greetings.",
        "example_sentence_zulu": "Hamba kahle.",
        "example_sentence_english": "Go well.",
        "example_sentence_swati": "Hamba kahle."
    },
    {
        "zulu_word": "Za",
        "english_translation": "Come",
        "swati_translation": "Ta",
        "pronunciation_guide": "ZAH",
        "part_of_speech": "verb",
        "cultural_context": "Basic verb for movement toward the speaker.",
        "example_sentence_zulu": "Za lapha.",
        "example_sentence_english": "Come here.",
        "example_sentence_swati": "Ta lapha."
    },
    {
        "zulu_word": "Dla",
        "english_translation": "Eat",
        "swati_translation": "Dla",
        "pronunciation_guide": "DLAH",
        "part_of_speech": "verb",
        "cultural_context": "Essential verb for nourishment and hospitality.",
        "example_sentence_zulu": "Sidla ukudla.",
        "example_sentence_english": "We eat food.",
        "example_sentence_swati": "Sidla kudla."
    },
    {
        "zulu_word": "Phuza",
        "english_translation": "Drink",
        "swati_translation": "Phuza",
        "pronunciation_guide": "PHOO-zah",
        "part_of_speech": "verb",
        "cultural_context": "Essential verb for drinking, often used in social contexts.",
        "example_sentence_zulu": "Ngiyaphuza amanzi.",
        "example_sentence_english": "I drink water.",
        "example_sentence_swati": "Ngiyaphuza emanti."
    },
    {
        "zulu_word": "Lala",
        "english_translation": "Sleep",
        "swati_translation": "Lala",
        "pronunciation_guide": "LAH-lah",
        "part_of_speech": "verb",
        "cultural_context": "Basic verb for rest and sleep.",
        "example_sentence_zulu": "Ngilala ebusuku.",
        "example_sentence_english": "I sleep at night.",
        "example_sentence_swati": "Ngilala ebusuku."
    },
    {
        "zulu_word": "Fundisa",
        "english_translation": "Teach",
        "swati_translation": "Fundzisa",
        "pronunciation_guide": "foon-DEE-sah",
        "part_of_speech": "verb",
        "cultural_context": "Verb for sharing knowledge, valued in oral tradition.",
        "example_sentence_zulu": "Umama uyangifundisa.",
        "example_sentence_english": "My mother teaches me.",
        "example_sentence_swati": "Make uyangifundzisa."
    },
    {
        "zulu_word": "Funda",
        "english_translation": "Learn/Read",
        "swati_translation": "Fundza",
        "pronunciation_guide": "FOON-dah",
        "part_of_speech": "verb",
        "cultural_context": "Verb for acquiring knowledge, important in education.",
        "example_sentence_zulu": "Ngifunda incwadi.",
        "example_sentence_english": "I read a book.",
        "example_sentence_swati": "Ngifundza incwadzi."
    },
    {
        "zulu_word": "Sebenza",
        "english_translation": "Work",
        "swati_translation": "Sebenta",
        "pronunciation_guide": "seh-BEN-zah",
        "part_of_speech": "verb",
        "cultural_context": "Verb for labor and productivity.",
        "example_sentence_zulu": "Ubaba usebenza emsebenzini.",
        "example_sentence_english": "Father works at his job.",
        "example_sentence_swati": "Babe usebenta emsebentini."
    },
    {
        "zulu_word": "Dlala",
        "english_translation": "Play",
        "swati_translation": "Dlala",
        "pronunciation_guide": "DLAH-lah",
        "part_of_speech": "verb",
        "cultural_context": "Verb for recreation and enjoyment.",
        "example_sentence_zulu": "Abantwana badlala ngaphandle.",
        "example_sentence_english": "The children play outside.",
        "example_sentence_swati": "Bantfwana badlala ngaphandle."
    },
    {
        "zulu_word": "Cula",
        "english_translation": "Sing",
        "swati_translation": "Cula",
        "pronunciation_guide": "CHOO-lah",
        "part_of_speech": "verb",
        "cultural_context": "Verb for musical expression, important in ceremonies.",
        "example_sentence_zulu": "Sicula ingoma.",
        "example_sentence_english": "We sing a song.",
        "example_sentence_swati": "Sicula ingoma."
    },
    {
        "zulu_word": "Dansa",
        "english_translation": "Dance",
        "swati_translation": "Dansa",
        "pronunciation_guide": "DAHN-sah",
        "part_of_speech": "verb",
        "cultural_context": "Verb for rhythmic movement, part of cultural expression.",
        "example_sentence_zulu": "Abantu badansa emcimbini.",
        "example_sentence_english": "People dance at the ceremony.",
        "example_sentence_swati": "Bantfu badansa emcimbini."
    },
    {
        "zulu_word": "Thetha",
        "english_translation": "Speak/Talk",
        "swati_translation": "Khuluma",
        "pronunciation_guide": "TEH-tah",
        "part_of_speech": "verb",
        "cultural_context": "Verb for communication and conversation.",
        "example_sentence_zulu": "Sithetha isiZulu.",
        "example_sentence_english": "We speak isiZulu.",
        "example_sentence_swati": "Sikhuluma siSwati."
    },
    {
        "zulu_word": "Lalela",
        "english_translation": "Listen",
        "swati_translation": "Lalela",
        "pronunciation_guide": "lah-LEH-lah",
        "part_of_speech": "verb",
        "cultural_context": "Verb for attentive hearing, important in oral tradition.",
        "example_sentence_zulu": "Ngilalela umama.",
        "example_sentence_english": "I listen to my mother.",
        "example_sentence_swati": "Ngilalela make."
    },
    {
        "zulu_word": "Bheka",
        "english_translation": "Look/See",
        "swati_translation": "Bheka",
        "pronunciation_guide": "BEH-kah",
        "part_of_speech": "verb",
        "cultural_context": "Verb for visual perception.",
        "example_sentence_zulu": "Bheka leyo nto.",
        "example_sentence_english": "Look at that thing.",
        "example_sentence_swati": "Bheka leyo ntfu."
    },
    {
        "zulu_word": "Cabanga",
        "english_translation": "Think",
        "swati_translation": "Cabanga",
        "pronunciation_guide": "cah-BAHN-gah",
        "part_of_speech": "verb",
        "cultural_context": "Verb for cognitive process and consideration.",
        "example_sentence_zulu": "Ngicabanga ngendaba.",
        "example_sentence_english": "I think about the matter.",
        "example_sentence_swati": "Ngicabanga ngendzaba."
    }
         ]
        
        # Add words to database
        for word_data in zulu_words:
            word, created = ZuluWord.objects.get_or_create(
                zulu_word=word_data['zulu_word'],
                defaults=word_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Added word: {word_data["zulu_word"]}')
                )
        
        # Create some word pairs
        word_pairs = [
            ('Sawubona', 'Hamba kahle'),
            ('Ubuntu', 'Indaba'),
            ('Imbeleko', 'Isidwaba'),
            ('Inyoni', 'Ukucula'),
            ('Ukubonga', 'Ukusiza'),
            ('Inhliziyo', 'Ukukhulekela'),
            ('Inkomo', 'Ukwelusa'),
            ('Inyanga', 'Ukwelapha'),
            ('Sawubona', 'Hamba kahle'),
        ('Yebo', 'Cha'),
        ('Umama', 'Ubaba'),
        ('Umfana', 'Intombi'),
        ('Hamba', 'Za'),
        ('Dla', 'Phuza'),
        ('Funda', 'Fundisa'),
        ('Thetha', 'Lalela'),
        ('Bheka', 'Cabanga'),
        ('Cula', 'Dansa'),
        ('Inja', 'Ikati'),
        ('Intaba', 'Umfula'),
        ('Umbila', 'Amazambane'),
        ('Ngiyabonga', 'Uxolo'),
        ('Unjani', 'Ngisaphila'),
        ]
        
        for word1, word2 in word_pairs:
            try:
                w1 = ZuluWord.objects.get(zulu_word=word1)
                w2 = ZuluWord.objects.get(zulu_word=word2)
                
                pair, created = WordPair.objects.get_or_create(
                    word1=w1,
                    word2=w2,
                    defaults={'frequency': 5}
                )
                
                if created:
                    self.stdout.write(
                        self.style.SUCCESS(f'Added word pair: {word1} - {word2}')
                    )
                else:
                    self.stdout.write(
                        self.style.WARNING(f'Word pair already exists: {word1} - {word2}')
                    )
            except ZuluWord.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'Could not find words for pair: {word1} - {word2}')
                )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully populated database with sample isiZulu data')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Total words in database: {ZuluWord.objects.count()}')
        )