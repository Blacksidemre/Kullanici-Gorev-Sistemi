# --- Blok 1: Kurulum ve Kütüphaneler ---
import gradio as gr
import json
import os
import datetime
import statistics

# --- Blok 2: Veri İşlem Fonksiyonları ---

def yukle_gorevler(kullanici):
    dosya = f"{kullanici}_gorevler.json"
    if not os.path.exists(dosya):
        return []
    try:
        with open(dosya, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []

def kaydet_gorevler(kullanici, gorevler):
    dosya = f"{kullanici}_gorevler.json"
    try:
        with open(dosya, "w", encoding="utf-8") as f:
            json.dump(gorevler, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Kaydetme hatası: {e}")
        return False

def istatistik_hesapla(gorevler):
    tamamlananlar = [g for g in gorevler if g.get("tamamlandi") and g.get("tamamlama_zamani")]
    sayi = len(tamamlananlar)
    if not sayi:
        return 0, 0.0

    sureler = []
    for g in tamamlananlar:
        try:
            bas = datetime.datetime.fromisoformat(g["olusturma_zamani"])
            bit = datetime.datetime.fromisoformat(g["tamamlama_zamani"])
            sureler.append((bit - bas).total_seconds() / 60)
        except (ValueError, TypeError):
            continue

    ort = statistics.mean(sureler) if sureler else 0.0
    return sayi, ort

# --- Blok 3: Yardımcı Fonksiyon ---

def gorev_listesi_formatla(gorevler):
    return [
        f"[{'✔️' if g['tamamlandi'] else '❌'}] {g['metin']}"
        for g in gorevler
    ]

# --- Blok 4: Arayüz Fonksiyonları ---

def login(user, pwd, state_user, state_gorevler):
    if not user or not pwd:
        return "Hata: Kullanıcı adı ve şifre gerekli", gr.update(choices=[], value=None), gr.update(visible=False), state_user, state_gorevler

    kayit = "users.json"
    users = {}
    if os.path.exists(kayit):
        try:
            with open(kayit, "r", encoding="utf-8") as f:
                users = json.load(f)
        except:
            users = {}

    if user in users and users[user] != pwd:
        return "Hata: Şifre yanlış", gr.update(choices=[], value=None), gr.update(visible=False), state_user, state_gorevler

    users[user] = pwd
    try:
        with open(kayit, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=4)
    except Exception as e:
        return f"Hata: Kullanıcı kaydedilemedi: {e}", gr.update(choices=[], value=None), gr.update(visible=False), state_user, state_gorevler

    yeni_gorevler = yukle_gorevler(user)
    formatlanmis_liste = gorev_listesi_formatla(yeni_gorevler)

    return (
        f"Giriş başarılı: {user}",
        gr.update(choices=formatlanmis_liste, value=None),
        gr.update(value="Görevler yüklendi.", visible=True),
        user,
        yeni_gorevler
    )

def gorev_ekle(metin, state_user, state_gorevler):
    if not state_user:
        return gr.update(choices=gorev_listesi_formatla(state_gorevler)), gr.update(value="Hata: Önce giriş yapmalısınız.", visible=True), gr.update(value=""), state_user, state_gorevler

    metin = metin.strip()
    if not metin:
        return gr.update(choices=gorev_listesi_formatla(state_gorevler)), gr.update(value="Hata: Boş görev eklenemez.", visible=True), gr.update(value=""), state_user, state_gorevler

    metin_duzeltilmis = metin.split('] ', 1)[-1] if metin.startswith('[') else metin

    yeni = {
        "id": int(datetime.datetime.now().timestamp()*1000),
        "metin": metin_duzeltilmis,
        "olusturma_zamani": datetime.datetime.utcnow().isoformat(),
        "tamamlandi": False,
        "tamamlama_zamani": None
    }

    state_gorevler.append(yeni)
    kaydet_gorevler(state_user, state_gorevler)

    formatlanmis_liste = gorev_listesi_formatla(state_gorevler)

    return (
        gr.update(choices=formatlanmis_liste, value=None),
        gr.update(value=f"'{metin_duzeltilmis}' eklendi.", visible=True),
        gr.update(value=""),
        state_user,
        state_gorevler
    )

def gorev_duzenle(metin_sec, yeni_metin, state_user, state_gorevler):
    if not state_user:
        return gr.update(choices=gorev_listesi_formatla(state_gorevler)), gr.update(value="Hata: Önce giriş yapmalısınız."), gr.update(value=""), state_user, state_gorevler

    if not metin_sec:
        return gr.update(choices=gorev_listesi_formatla(state_gorevler)), gr.update(value="Hata: Düzenlemek için görev seçmelisiniz."), gr.update(value=yeni_metin), state_user, state_gorevler

    yeni_metin = yeni_metin.strip()
    if not yeni_metin:
        return gr.update(choices=gorev_listesi_formatla(state_gorevler)), gr.update(value="Hata: Yeni görev metni boş olamaz."), gr.update(value=""), state_user, state_gorevler

    gorev_metni = metin_sec.split('] ', 1)[-1]
    g = next((g for g in state_gorevler if g["metin"] == gorev_metni), None)

    if g:
        g['metin'] = yeni_metin
        kaydet_gorevler(state_user, state_gorevler)
        formatlanmis_liste = gorev_listesi_formatla(state_gorevler)
        return (
            gr.update(choices=formatlanmis_liste, value=None),
            gr.update(value="Görev güncellendi."),
            gr.update(value=""),
            state_user,
            state_gorevler
        )
    else:
        return gr.update(choices=gorev_listesi_formatla(state_gorevler)), gr.update(value="Hata: Görev bulunamadı."), gr.update(value=""), state_user, state_gorevler

def gorev_toggle(metin_sec, state_user, state_gorevler):
    if not state_user or not metin_sec:
        return gr.update(choices=gorev_listesi_formatla(state_gorevler)), state_user, state_gorevler

    gorev_metni = metin_sec.split('] ', 1)[-1]
    g = next((g for g in state_gorevler if g["metin"] == gorev_metni), None)

    if g:
        if not g["tamamlandi"]:
            g["tamamlandi"] = True
            g["tamamlama_zamani"] = datetime.datetime.utcnow().isoformat()
        else:
            g["tamamlandi"] = False
            g["tamamlama_zamani"] = None
        kaydet_gorevler(state_user, state_gorevler)

    formatlanmis_liste = gorev_listesi_formatla(state_gorevler)
    return gr.update(choices=formatlanmis_liste, value=None), state_user, state_gorevler

def gorev_sil(metin_sec, state_user, state_gorevler):
    if not state_user or not metin_sec:
        return gr.update(choices=gorev_listesi_formatla(state_gorevler)), state_user, state_gorevler

    gorev_metni = metin_sec.split('] ', 1)[-1]

    yeni_gorevler = [g for g in state_gorevler if g["metin"] != gorev_metni]
    kaydet_gorevler(state_user, yeni_gorevler)

    formatlanmis_liste = gorev_listesi_formatla(yeni_gorevler)
    return gr.update(choices=formatlanmis_liste, value=None), state_user, yeni_gorevler

def goster_istatistik(state_user, state_gorevler):
    if not state_user:
        return "Önce giriş yapmalısınız"
    tamam, ort = istatistik_hesapla(state_gorevler)
    return f"Tamamlanan görev sayısı: {tamam}\nOrtalama süre: {ort:.2f} dakika" if tamam else "Henüz tamamlanan görev yok."

# --- Blok 5 + 6: Arayüz ve Etkileşimler ---

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 📋 Çok Kullanıcılı Görev Yönetim Uygulaması")

    current_user_state = gr.State(None)
    gorevler_state = gr.State([])

    with gr.Row():
        user_input = gr.Textbox(label="Kullanıcı adı", scale=2)
        pwd_input = gr.Textbox(label="Şifre", type="password", scale=2)
        login_btn = gr.Button("Giriş Yap / Kayıt Ol", scale=1)

    login_status = gr.Textbox(label="Durum", interactive=False)

    with gr.Column(visible=False) as task_column:
        gr.Markdown("---")
        gr.Markdown("### Görev Yönetimi")

        with gr.Row():
            task_input = gr.Textbox(label="Yeni Görev Ekle / Düzenle", scale=3)
            add_btn = gr.Button("➕ Ekle", scale=1)

        task_list = gr.Dropdown(
            choices=[], label="Görevler",
            interactive=True, type="value", value=None
        )

        with gr.Row():
            toggle_btn = gr.Button("✅ Tamamla / Geri Al", scale=1)
            edit_btn = gr.Button("✏️ Düzenle", scale=1)
            del_btn = gr.Button("🗑️ Sil", scale=1, variant="stop")

        mesaj = gr.Textbox(label="Mesaj", interactive=False, value="")

        gr.Markdown("---")
        gr.Markdown("### İstatistikler")
        stat_btn = gr.Button("📊 İstatistikleri Göster")
        stat_out = gr.Textbox(label="İstatistik", interactive=False)

    def update_visibility(status):
        return gr.update(visible=status.startswith("Giriş başarılı"))

    login_btn.click(
        fn=login,
        inputs=[user_input, pwd_input, current_user_state, gorevler_state],
        outputs=[login_status, task_list, mesaj, current_user_state, gorevler_state]
    ).then(
        fn=update_visibility,
        inputs=[login_status],
        outputs=[task_column]
    )

    add_btn.click(
        fn=gorev_ekle,
        inputs=[task_input, current_user_state, gorevler_state],
        outputs=[task_list, mesaj, task_input, current_user_state, gorevler_state]
    )

    edit_btn.click(
        fn=gorev_duzenle,
        inputs=[task_list, task_input, current_user_state, gorevler_state],
        outputs=[task_list, mesaj, task_input, current_user_state, gorevler_state]
    )

    toggle_btn.click(
        fn=gorev_toggle,
        inputs=[task_list, current_user_state, gorevler_state],
        outputs=[task_list, current_user_state, gorevler_state]
    )

    del_btn.click(
        fn=gorev_sil,
        inputs=[task_list, current_user_state, gorevler_state],
        outputs=[task_list, current_user_state, gorevler_state]
    )

    stat_btn.click(
        fn=goster_istatistik,
        inputs=[current_user_state, gorevler_state],
        outputs=[stat_out]
    )

demo.launch(debug=True)
