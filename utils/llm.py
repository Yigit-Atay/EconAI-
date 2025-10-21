import os
import re
import wikipediaapi

# ——— Wikipedia istemcisi ———
WIKI = wikipediaapi.Wikipedia(
    language="tr",
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent="EconAI/1.0 (https://github.com/Yigit-Atay; contact: yigitatay1@hotmail.com)",
)

ECON_PERSONA = (
    "Sen EconAI adlı bir iktisat asistanısın. "
    "Odak alanların: mikroekonomi, makroekonomi, para politikası, istatistik, ekonometrik analiz ve finans. "
    "Gerçek ve doğrulanabilir bilgi kullan; mümkünse kısa kaynak/ekol belirt (Keynesyen, Monetarist vb.). "
    "Sonunda 1–2 cümlelik özet ekle."
)

def _wiki_summary(query: str) -> str | None:
    # Aramayı sadeleştir
    q = query.strip()
    # Doğrudan sayfa dene
    page = WIKI.page(q)
    if page.exists():
        text = page.summary
        return text if text else None
    # Bazı yaygın varyantlar
    for alt in [q.capitalize(), q.lower(), q.title()]:
        p = WIKI.page(alt)
        if p.exists():
            return p.summary or None
    return None

def _format_answer(body: str) -> str:
    body = body.strip()
    # Kısa özet ekle
    tail = "\n\n**Özet:** Yukarıdaki açıklama, temel kavramları ve ilişkileri kısaca derler."
    return body + tail

def gpt_answer(query: str) -> str:
    """
    1) OPENAI_API_KEY varsa GPT-4o-mini ile yanıt
    2) Yoksa Wikipedia özeti + şık bir format
    Ekonomi dışı sorularda, kibar yönlendirme yapar.
    """
    econ_keywords = ["ekonomi","iktisat","finans","para","enflasyon","faiz",
    "banka","TCMB","FED","yatırım","borsa","kripto","gsyh","işsizlik"
    "döviz","tahvil","hisse","sermaye","maliye","vergi",
    "ticaret","dış ticaret","cari açık","bütçe","tasarruf",
    "tüketim","arz","talep","piyasa","makroekonomi","mikroekonomi",
    "ekonomik büyüme","resesyon","döngü","küresel ekonomi",
    "finansal kriz","likidite","enflasyon hedeflemesi",
    "para politikası","maliye politikası",
    "ekonomik göstergeler","iş gücü","ücret","gelir dağılımı",
    "sermaye piyasası","finansal araçlar",
    "yatırım fonu","borsa endeksi","döviz kuru",
    "kripto para","blockchain","fintech","ekonometrik",
    "arz şoku","talep şoku","ekonomik model","piyasa dengesi",
    "tüketici güveni","üretici fiyatları",
    "küresel ticaret","ekonomik entegrasyon",
    "sürdürülebilir kalkınma","yeşil ekonomi",
    "döngüsel ekonomi","karbon ayak izi",
    "iklim değişikliği","doğa dostu",
    "sıfır atık","döngüsel tasarım",
    "sürdürülebilir finans",
    "yeşil tahvil","çevresel, sosyal ve yönetişim (ESG)",
    "sosyal etki yatırımı","sürdürülebilirlik raporlaması",
    "yeşil enerji","yenilenebilir enerji",
    "enerji verimliliği","karbon ticareti",
    "iklim finansmanı","karbon nötrlük","çevre politikası",
    "yeşil büyüme","sürdürülebilir kalkınma hedefleri","yeşil inovasyon",
    "bitcoin","ethereum","defi","nft","stablecoin","metaverse","web3","altcoin",
    "block zinciri","kripto borsa","madencilik","cüzdan","tokenizasyon","altın",
    "gümüş","emtia","hammadde","piyasa analizi","teknik analiz","temel analiz",
    "portföy yönetimi","risk yönetimi","varlık tahsisi","finansal planlama",
    "emeklilik planlaması","vergi planlaması","miras planlaması",
    "finansal danışmanlık","yatırım stratejisi","piyasa trendleri",
    "ekonomik tahmin","küresel piyasa","finansal regülasyon","merkez bankası",
    "para arzı","döviz rezervi","makroekonomik politika","küresel finans",
    "finansal istikrar","ekonomik reform","yapısal dönüşüm","ekonomik kalkınma",
    "sosyal politika","iş gücü piyasası","insan sermayesi","eğitim ekonomisi",
    "sağlık ekonomisi","kentsel ekonomi","bölgesel kalkınma","tarım ekonomisi",
    "enerji ekonomisi","çevre ekonomisi","ulaştırma ekonomisi","turizm ekonomisi",
    "davranışsal ekonomi","deneysel ekonomi","oyun teorisi","bilgisayar ekonomisi",
    "veri analitiği","büyük veri","yapay zeka ekonomisi","makine öğrenimi ekonomisi",
    "blok zinciri ekonomisi","sanal para birimi","dijital ekonomi","internet ekonomisi",
    "e-ticaret","mobil ekonomi","paylaşım ekonomisi","gig ekonomisi",
    "platform ekonomisi","sosyal medya ekonomisi","dijital pazarlama","çevrimiçi reklamcılık",
    "siber güvenlik ekonomisi","veri gizliliği ekonomisi","dijital dönüşüm ekonomisi",
    ]

    is_econ = any(k in query.lower() for k in econ_keywords)

    # 1) OpenAI var mı?
    api_key = os.getenv("OPENAI_API_KEY", "").strip()
    if api_key:
        try:
            from openai import OpenAI
            client = OpenAI(api_key=api_key)
            sys = ECON_PERSONA + (
                " Ekonomi dışı bir soruysa kibarca yönlendir: "
                "'Bu asistan iktisat/finans odaklıdır.'"
            )
            msgs = [
                {"role": "system", "content": sys},
                {"role": "user", "content": query},
            ]
            resp = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=msgs,
                temperature=0.2,
                max_tokens=600,
            )
            txt = resp.choices[0].message.content.strip()
            return txt
        except Exception as e:
            # OpenAI hata verirse Wikipedia’ya düş
            pass

    # 2) Wikipedia fallback
    if not is_econ:
        return ("Bu asistan **iktisat ve finans** odaklıdır. "
                "Ekonomiyle ilişkili biçimde sorarsan daha güçlü yanıt veririm. 🙂")

    summ = _wiki_summary(query)
    if summ:
        return _format_answer(summ)

    return ("Bu başlığa dair Wikipedia özetine ulaşamadım. "
            "Dilersen terimi biraz daha spesifikleştir: örn. 'Phillips eğrisi enflasyon' gibi.")
