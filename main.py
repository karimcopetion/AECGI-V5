import streamlit as st
import requests
import time

# =================================================================
# 🔑 SHYIRAMO API KEY YAWE HANO (HARDCODED)
# Siba iri jambo riri mu dukandiko, upastemo ya Key yawe yose ihera ku bimenyetso r8_
# =================================================================
REPLICATE_API_KEY = "r8_Shyiramo_Ya_Key_Yawe_Hano_Yose_Yuzuye"


# --- 1. DESIGN N'ISHUSHO YA WEBSITE (UI CONFIG) ---
st.set_page_config(
    page_title="AECGI Free AI Engine", 
    page_icon="🎬", 
    layout="wide"
)

# Isura ya Kinyamwuga ya AECGI Studio
st.title("🎬 AECGI FREE AI VIDEO ENGINE v12.0")
st.subheader("Hollywood-Grade Animation Studio (Direct API Node)")
st.write("Urubuga rwa Kinyamwuga rwo Gukora Video z'Ubuntu Ukoresheje AI")

st.markdown("---")

# --- 2. SIDEBAR INFO ---
st.sidebar.header("⚙️ AECGI Core Status")
st.sidebar.success("✅ AECGI Engine is connected directly to Replicate!")
st.sidebar.markdown("---")
st.sidebar.info(
    "ℹ️ Kuri iyi nshuro, API Key yashizwemo imbere muri code mu buryo bw'ibanga. "
    "Wowe icyo usabwa gukora gusa ni ukwandika prompt ukiyuburura!"
)

# --- 3. THE MAIN VIDEO ENGINE ---
st.header("🎞️ Generator & Prompt Studio")
st.write("Andika Prompt (Ibisobanuro), uheze ukande buto ngo AI iguhe video handles.")

# Umwanya wo kwandika prompt
ai_editing_prompt = st.text_area(
    "Andika Prompt ya Video hano (Mu Cyongereza):",
    placeholder="Urugero: A high-speed sports car racing through Kigali streets, photorealistic, cinematic lighting, 4k resolution..."
)

st.markdown("###")

# --- 4. TANGIRA GUKORA VIDEO ---
if st.button("🚀 Tangira Gukora Video") and ai_editing_prompt:
    # Genzura niba muser atari we wibagiwe guhindura ya Key muli code
    if "Shyiramo_Ya_Key_Yawe_Hano" in REPLICATE_API_KEY:
        st.error("⚠️ Umwubatsi mukuru, wibagiwe gushyira ya Key yawe nyayo muli code aho handitse 'REPLICATE_API_KEY'!")
    else:
        with st.spinner("AECGI AI Core iri gukorana na Server za Replicate... Tegereza gato..."):
            try:
                headers = {
                    "Authorization": f"Token {REPLICATE_API_KEY}",
                    "Content-Type": "application/json"
                }
                
                # Modeli y'ubuntu idasaba credit muli Replicate
                data = {
                    "version": "392f6699127431114346340426d7b21efc163a1211bc99734a1d831b26551b74", 
                    "input": {
                        "prompt": ai_editing_prompt,
                        "num_frames": 14,
                        "fps": 6
                    }
                }
                
                # Kohereza Itegeko kuri Replicate
                response = requests.post("https://api.replicate.com/v1/predictions", headers=headers, json=data)
                res_json = response.json()
                
                prediction_id = res_json.get("id")
                
                if prediction_id:
                    status = "starting"
                    ai_video_url = ""
                    
                    # Gukurikiranira hafi niba video yuzuye (Polling loop)
                    while status not in ["succeeded", "failed"]:
                        time.sleep(4)
                        check_res = requests.get(f"https://api.replicate.com/v1/predictions/{prediction_id}", headers=headers)
                        status = check_res.json().get("status")
                        
                        if status == "succeeded":
                            ai_video_url = check_res.json().get("output")
                            break
                        elif status == "failed":
                            break
                    
                    if ai_video_url:
                        st.success("✅ Video yawe y'ubuntu iruzuye neza kandi irarangiye!")
                        
                        # Kwerekana Video yuzuye kuri Website
                        if isinstance(ai_video_url, list):
                            st.video(ai_video_url[0])
                        else:
                            st.video(ai_video_url)
                            
                        st.balloons()
                    else:
                        st.error("⚠️ Server yanze gupfunda video. Ongera ugerageze gato.")
                else:
                    # Niba rero na n'ubu yanze, bivuze ko Key iri muli code ifite ikosa rya Copy-Paste
                    st.error("⚠️ Replicate yanze iyi API Key iri muli code. Genzura neza niba nta nyuguti wasize inyuma umaze kuyikopiya.")
            except Exception as e:
                st.error(f"⚠️ Haza ikosa mu mivugururire: {e}")
