"""
build_zu_mo.py — Compile an isiZulu .mo catalogue without GNU gettext.

Run from the project root:

    python build_zu_mo.py

It writes:  locale/zu/LC_MESSAGES/django.mo
"""
import pathlib
import struct

# ---------------------------------------------------------------------------
# msgid → msgstr mapping (isiZulu)
# ---------------------------------------------------------------------------
TRANSLATIONS = {
    # ── Brand & navigation ─────────────────────────────────────────────
    "IsiZulu Cultural Corpus": "IsiZulu Cultural Corpus",
    "IsiZulu Cultural": "IsiZulu Cultural",
    "Corpus": "Ikhophasi",
    "LANGUAGE & HERITAGE": "ULIMI NAMAGUGU",
    "Home": "Ikhaya",
    "Search": "Sesha",
    "Favourites": "Izintandokazi",
    "History": "Umlando",
    "Trends": "Izitayela",
    "Cultural Stories": "Izindaba Zamasiko",
    "Help": "Usizo",
    "Profile": "Iphrofayela",
    "Login": "Ngena",
    "Register": "Bhalisa",
    "Your Profile": "Iphrofayela Yakho",
    "Language": "Ulimi",
    "English": "IsiNgisi",
    "IsiZulu": "IsiZulu",

    # ── Home page ──────────────────────────────────────────────────────
    "YOUR CULTURAL LIBRARY": "ILAYIBRARI YAKHO YAMASIKO",
    "Welcome, %(name)s. Continue exploring isiZulu language and culture.":
        "Siyakwamukela, %(name)s. Qhubeka uhlola ulimi lwesiZulu namasiko.",
    "Explore language.": "Hlola ulimi.",
    "Connect with culture.": "Xhumana namasiko.",
    "A space for isiZulu words, their English meanings, and the cultural stories that connect them.":
        "Indawo yamagama esiZulu, izincazelo zawo zesiNgisi, kanye nezindaba zamasiko ezixhumanisa wona.",
    "Search an isiZulu word or English meaning":
        "Sesha igama lesiZulu noma incazelo yesiNgisi",
    "Keep the words you want to return to.":
        "Gcina amagama ofuna ukuwabuyela kuwo.",
    "Explore the culture behind the language.":
        "Hlola amasiko angemuva kolimi.",
    "Explore Cultural Stories": "Hlola Izindaba Zamasiko",
    "Discover searches and corpus statistics.":
        "Thola izibalo zokusesha nekhophasi.",
    "View Trends": "Buka Izitayela",
    "Your Search History": "Umlando Wakho Wokusesha",
    "View History": "Buka Umlando",
    "No searches yet. Start exploring the corpus!":
        "Akukho okuseshiwe okwamanje. Qala ukuhlola ikhophasi!",

    # ── Search page ────────────────────────────────────────────────────
    "EXPLORE THE CORPUS": "HLOLE IKHOPHASI",
    "Find isiZulu words and expressions, with their English meanings side by side.":
        "Thola amagama nezisho zesiZulu, kanye nezincazelo zazo zesiNgisi eceleni.",
    "Search for a word, phrase or meaning…":
        "Sesha igama, ibinzana noma incazelo…",
    "Search in": "Sesha ku",
    "Both languages": "Zombili izilimi",
    "Search a word or part of an expression.":
        "Sesha igama noma ingxenye yesisho.",
    "Listen to a word · Save with the star":
        "Lalela igama · Gcina ngenkanyezi",
    "English meaning": "Incazelo yesiNgisi",
    "No results for": "Ayikho imiphumela ye",
    "Did you mean:": "Ube uqonde:",
    "Check the spelling, or try a different language.":
        "Hlola isipelingi, noma uzame olunye ulimi.",
    "Hear the pronunciation": "Zwa ukuphimisela",
    "Use the speaker icon next to an isiZulu word. Pronunciation may not always be accurate.":
        "Sebenzisa isithonjana sesipikha eduze kwegama lesiZulu. Ukuphimisela kungase kungabi ncophelela ngaso sonke isikhathi.",
    "Download the Corpus Database": "Landa Isizindalwazi Sekhophasi",
    "Download the complete database as a JSON file (requires login).":
        "Landa isizindalwazi esiphelele njengefayela le-JSON (kudinga ukungena).",
    "Download Database": "Landa Isizindalwazi",

    # ── History page ───────────────────────────────────────────────────
    "PICK UP WHERE YOU LEFT OFF": "QHUBEKA LAPHO USHIYE KHONA",
    "Your %(count)s most recent distinct searches. Searching the same term again moves it to the top instead of adding a duplicate.":
        "Izinto zakho ezingu-%(count)s ezisanda kuseshwa ezihlukile. Ukusesha igama elifanayo futhi kuyisa phezulu esikhundleni sokwengeza okufanayo.",
    "Clear All History": "Sula Wonke Umlando",
    "Found": "Kutholakale",
    "Search Again": "Sesha Futhi",
    "Remove": "Susa",
    "No results were found for this search.":
        "Ayikho imiphumela eyatholakala kulokhu kusesha.",
    "Your search history is empty.":
        "Umlando wakho wokusesha awunalutho.",
    "Start exploring the": "Qala ukuhlola",
    "corpus": "ikhophasi",
    "to build your history!": "ukwakha umlando wakho!",
    "History is private to your account and keeps your 5 most recent distinct searches. Remove a single entry or clear your whole history.":
        "Umlando uyimfihlo ye-akhawunti yakho futhi ugcina izinto zakho ezi-5 ezisanda kuseshwa ezihlukile. Susa into eyodwa noma usule wonke umlando wakho.",

    # ── Trends page ────────────────────────────────────────────────────
    "A LOOK AT THE CORPUS": "UKUBHEKA IKHOPHASI",
    "Corpus Statistics And Trends": "Izibalo Nezitayela Zekhophasi",
    "Explore overall corpus statistics, frequently searched words and common word pairs.":
        "Hlola izibalo zekhophasi iyonke, amagama avame ukuseshwa kanye namagama amabili avamile.",
    "Total Words": "Amagama Ewonke",
    "Total Phrases": "Imisho Ewonke",
    "Total Users": "Abasebenzisi Abonke",
    "Total Searches": "Ukusesha Okuphelele",
    "Most Frequent Words": "Amagama Avame Kakhulu",
    "Search counts for the most frequent entries in the table below.":
        "Izibalo zokusesha zezinto ezivame kakhulu kuthebula elingezansi.",
    "Search Frequency": "Imvamisa Yokusesha",
    "Word Statistics": "Izibalo Zamagama",
    "displayed entries": "izinto ezibonisiwe",
    "Word · IsiZulu": "Igama · IsiZulu",
    "Translation · English": "Ukuhumusha · IsiNgisi",
    "Search Count": "Inani Lokusesha",
    "Part of Speech": "Ingxenye Yenkulumo",
    "Common Word Pairs": "Amagama Amabili Avamile",
    "Words that have appeared together in the same search results.":
        "Amagama avela ndawonye emiphumeleni yokusesha efanayo.",
    "Word 1": "Igama 1",
    "Word 2": "Igama 2",
    "Frequency": "Imvamisa",
    "No word pairs recorded yet — search for a term that matches more than one word to build this table.":
        "Awekho amagama amabili aqoshiwe okwamanje — sesha igama elihambisana namagama angaphezu kwelilodwa ukwakha leli thebula.",
    "No data available.": "Ayikho idatha etholakalayo.",
    "No search data yet.": "Ayikho idatha yokusesha okwamanje.",

    # ── Help page ──────────────────────────────────────────────────────
    "MAKE THE MOST OF THE CORPUS": "SEBENZISA IKHOPHASI NGEZONKE IZINDLELA",
    "A simple guide to pronunciation, favourites, trends and your search history.":
        "Umhlahlandlela olula wokuphimisela, izintandokazi, izitayela nomlando wakho wokusesha.",
    "Pronunciation": "Ukuphimisela",
    "Click the speaker icon next to any isiZulu word to hear its pronunciation. For best results:":
        "Chofoza isithonjana sesipikha eduze kwanoma yiliphi igama lesiZulu ukuzwa ukuphimisela kwalo. Ukuze uthole imiphumela emihle:",
    "Use a modern browser that supports speech synthesis.":
        "Sebenzisa isiphequluli sesimanje esisekela ukwakhiwa kwenkulumo.",
    "Ensure your volume is turned on.":
        "Qiniseka ukuthi ivolumu yakho ivuliwe.",
    "isiZulu voices may not be available in all browsers.":
        "Amazwi esiZulu kungenzeka angatholakali kuzo zonke iziphequluli.",
    "Please note that the pronunciation may not always be accurate.":
        "Sicela uqaphele ukuthi ukuphimisela kungase kungabi ncophelela ngaso sonke isikhathi.",
    "Saving Favourites": "Ukugcina Izintandokazi",
    "Click the star icon next to any word to add it to your favourites. You can:":
        "Chofoza isithonjana senkanyezi eduze kwanoma yiliphi igama ukuze ulengeze ezintandokazini zakho. Ungakwenza:",
    "Access your favourites from the Favourites page.":
        "Finyelela izintandokazi zakho kusukela ekhasini lezintandokazi.",
    "Remove words by clicking the star again.":
        "Susa amagama ngokuchofoza inkanyezi futhi.",
    "Use favourites to build your personal vocabulary list.":
        "Sebenzisa izintandokazi ukwakha uhlu lwakho lwamagama.",
    "Select the star to save a word": "Khetha inkanyezi ukugcina igama",
    "Viewing Trends": "Ukubuka Izitayela",
    "The Trends page shows statistics about the corpus:":
        "Ikhasi lezitayela libonisa izibalo mayelana nekhophasi:",
    "Most frequently searched words.":
        "Amagama avame ukuseshwa kakhulu.",
    "Common word pairs.": "Amagama amabili avamile.",
    "Overall corpus statistics.": "Izibalo zekhophasi iyonke.",
    "Search History": "Umlando Wokusesha",
    "The History page keeps your 5 most recent distinct searches, newest first. Searching the same term again moves it to the top rather than adding a duplicate.":
        "Ikhasi lomlando ligcina izinto zakho ezi-5 ezisanda kuseshwa ezihlukile, ezintsha kuqala. Ukusesha igama elifanayo futhi kuyisa phezulu esikhundleni sokwengeza okufanayo.",
    "You can remove a single entry or clear your whole history. History is private to your account.":
        "Ungasusa into eyodwa noma usule wonke umlando wakho. Umlando uyimfihlo ye-akhawunti yakho.",
    "Downloading the Corpus": "Ukulanda Ikhophasi",
    "The corpus is available as a JSON file. You need to be logged in to download it.":
        "Ikhophasi itholakala njengefayela le-JSON. Udinga ukungena ukuze uyilande.",
    "Download Corpus": "Landa Ikhophasi",

    # ── Profile page ───────────────────────────────────────────────────
    "YOUR PERSONAL LIBRARY": "ILAYIBRARI YAKHO SIBO",
    "Your account information and recent activity, all in one place.":
        "Imininingwane ye-akhawunti yakho nomsebenzi wakamuva, konke endaweni eyodwa.",
    "Account Information": "Imininingwane Ye-akhawunti",
    "Username": "Igama lomsebenzisi",
    "Email": "I-imeyili",
    "Joined": "Wajoyina",
    "Not provided": "Ayikunikezwanga",
    "Your history stays yours": "Umlando wakho uhlala ungowakho",
    "Search history is private to your account. You can remove entries from History at any time.":
        "Umlando wokusesha uyimfihlo ye-akhawunti yakho. Ungasusa izinto kuMlando noma nini.",
    "Logout": "Phuma",
    "Your Activity": "Umsebenzi Wakho",
    "Favourite Words": "Amagama Ayizintandokazi",
    "Searches": "Ukusesha",
    "Recent Activity": "Umsebenzi Wakamuva",
    "Searched for": "Kuseshwe",
    "No recent activity to display.": "Awukho umsebenzi wakamuva ozoboniswa.",

    # ── Favourites page ────────────────────────────────────────────────
    "YOUR SAVED WORDS": "AMAGAMA AKHO AGCIWE",
    "Words you've saved for later. Tap the star to remove them.":
        "Amagama owagcine kamuva. Thepha inkanyezi ukuwasusa.",
    "Search your favourites…": "Sesha ezintandokazini zakho…",
    "Search favourites": "Sesha izintandokazi",
    "No favourites match": "Azikho izintandokazi ezihambisana ne",
    "Clear search": "Sula ukusesha",
    "to see all your favourites.": "ukubona zonke izintandokazi zakho.",
    "No Favourites Yet": "Azikho Izintandokazi Okwamanje",
    "You haven't added any words to your favourites yet.":
        "Awukangeze wengeza amagama ezintandokazini zakho.",
    "to find words to save!": "ukuthola amagama okuwagcina!",

    # ── Cultural stories page ──────────────────────────────────────────
    "STORIES BEHIND THE LANGUAGE": "IZINDABA EZINGEMUVA KOLIMI",
    "Traditional foods, wild fruits, ceremonies, and the life of the Zulu people in the past.":
        "Ukudla kwendabuko, izithelo zasendle, imicimbi, kanye nempilo yabantu bakwaZulu emandulo.",
    "Download the Cultural Stories Document":
        "Landa Idokhumenti Yezindaba Zamasiko",
    "Includes content in isiZulu, English, Sesotho and Siswati.":
        "Kuhlanganisa okuqukethwe ngesiZulu, isiNgisi, iSesotho nesiSwati.",
    "Download Cultural Stories (DOCX)": "Landa Izindaba Zamasiko (DOCX)",

    # ── Auth pages ─────────────────────────────────────────────────────
    "Sign in to access your favourites, history and personal library.":
        "Ngena ukuze ufinyelele izintandokazi zakho, umlando kanye nelayibrari yakho sibo.",
    "Your username and password didn't match. Please try again.":
        "Igama lakho lomsebenzisi nephasiwedi azihambisani. Sicela uzame futhi.",
    "Password": "Iphasiwedi",
    "Don't have an account?": "Awunayo i-akhawunti?",
    "Register here": "Bhalisa lapha",
    "Create an account to save favourites and track your searches.":
        "Dala i-akhawunti ukugcina izintandokazi nokulandelela ukusesha kwakho.",
    "Please correct the errors below.":
        "Sicela ulungise amaphutha angezansi.",
    "Password Confirmation": "Ukuqinisekiswa KwePhasiwedi",
    "Already have an account?": "Usunayo i-akhawunti?",
    "Login here": "Ngena lapha",

    # ── Word detail page ───────────────────────────────────────────────
    "Details": "Imininingwane",
    "Cultural Context": "Umongo Wamasiko",
    "Example Usage (isiZulu)": "Isibonelo Sokusetshenziswa (isiZulu)",
    "Word Usage": "Ukusetshenziswa Kwegama",
    "Phrases": "Imisho",
    "Synonyms": "Amagama Afanayo",
    "No usage examples available.":
        "Azikho izibonelo zokusetshenziswa ezitholakalayo.",
    "No common phrases found.": "Ayikho imisho evamile etholakele.",
    "No synonyms available.": "Awekho amagama afanayo atholakalayo.",

    # ── Messages ───────────────────────────────────────────────────────
    "Registration successful!": "Ukubhalisa kuphumelele!",
    "History entry not found.": "Into yomlando ayitholakalanga.",
    "Search history entry removed.": "Into yomlando wokusesha isusiwe.",
    "Cleared %(count)d history entries.":
        "Kusulwe izinto zomlando ezingu-%(count)d.",
    "Added to favourites": "Kungezwe ezintandokazini",
    "Removed from favourites": "Kususwe ezintandokazini",
    "Word not found.": "Igama alitholakalanga.",
    "Invalid request method. Only POST allowed.":
        "Indlela yesicelo engavumelekile. Kuphela i-POST evunyelwe.",
    "Please log in to save favourites.":
        "Sicela ungene ukuze ugcine izintandokazi.",

    # ── Footer ─────────────────────────────────────────────────────────
    "isiZulu entries · English meanings":
        "Okufakwe ngesiZulu · Izincazelo zesiNgisi",
}


# ---------------------------------------------------------------------------
# .mo file writer
# ---------------------------------------------------------------------------
def _u32(n):
    return struct.pack("<I", n)


def write_mo(translations, out_path):
    # Ensure the header entry exists (metadata block)
    header = (
        "Project-Id-Version: IsiZulu Cultural Corpus 1.0\n"
        "Language: zu\n"
        "MIME-Version: 1.0\n"
        "Content-Type: text/plain; charset=UTF-8\n"
        "Content-Transfer-Encoding: 8bit\n"
        "Plural-Forms: nplurals=2; plural=(n != 1);\n"
    ).encode("utf-8")

    entries = [(b"", b"", header)]
    for msgid, msgstr in translations.items():
        entries.append((msgid.encode("utf-8"), b"", msgstr.encode("utf-8")))

    # Sort by msgid (required by the .mo spec)
    entries.sort(key=lambda e: e[0])

    # Compute offsets
    n = len(entries)
    table_start = 28
    orig_table_size = 8 * n
    trans_table_size = 8 * n
    body_start = table_start + orig_table_size + trans_table_size

    orig_table = b""
    trans_table = b""
    body = b""

    cur = body_start
    for msgid, _ctx, msgstr in entries:
        orig_table += _u32(len(msgid)) + _u32(cur)
        cur += len(msgid) + 1
        trans_table += _u32(len(msgstr)) + _u32(cur)
        cur += len(msgstr) + 1

    for msgid, _ctx, msgstr in entries:
        body += msgid + b"\x00" + msgstr + b"\x00"

    header_bytes = (
        _u32(0x950412DE)                       # magic number
        + _u32(0)                              # format revision
        + _u32(n)                              # number of strings
        + _u32(table_start)                    # offset of original table
        + _u32(table_start + orig_table_size)  # offset of translation table
        + _u32(0)                              # hash table size
        + _u32(0)                              # hash table offset
    )

    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(header_bytes + orig_table + trans_table + body)


if __name__ == "__main__":
    out = pathlib.Path("locale/zu/LC_MESSAGES/django.mo")
    write_mo(TRANSLATIONS, out)
    print(f"Wrote {out}  ({out.stat().st_size} bytes, {len(TRANSLATIONS)} strings)")