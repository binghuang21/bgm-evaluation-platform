from flask import Flask, render_template, redirect, url_for, request, send_from_directory
import os
import time
import subprocess

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['INFERENCE_FOLDER'] = 'inference'
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
if not os.path.exists(app.config['INFERENCE_FOLDER']):
    os.makedirs(app.config['INFERENCE_FOLDER'])
app.config['TXT_FOLDER'] = 'txts'
if not os.path.exists(app.config['TXT_FOLDER']):
    os.makedirs(app.config['TXT_FOLDER'])
app.config['CREATER_TXT_FOLDER'] = 'create_txts'
if not os.path.exists(app.config['CREATER_TXT_FOLDER']):
    os.makedirs(app.config['CREATER_TXT_FOLDER'])
app.config['VIDEO_FOLDER'] = 'inference_our'
if not os.path.exists(app.config['VIDEO_FOLDER']):
    os.makedirs(app.config['VIDEO_FOLDER'])
app.config['CMT_VIDEO_FOLDER'] = 'inference_cmt'
if not os.path.exists(app.config['CMT_VIDEO_FOLDER']):
    os.makedirs(app.config['CMT_VIDEO_FOLDER'])

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/user')
def user():
    videos = os.listdir(app.config['VIDEO_FOLDER'])
    cmt_videos = os.listdir(app.config['CMT_VIDEO_FOLDER'])
    return render_template('user.html', videos=videos, cmt_videos=cmt_videos)


@app.route('/video/<path:filename>')
def video(filename):
    return send_from_directory(app.config['VIDEO_FOLDER'], filename)


@app.route('/cmt_video/<path:filename>')
def cmt_video(filename):
    return send_from_directory(app.config['CMT_VIDEO_FOLDER'], filename)


@app.route('/creater')
def creater():
    return render_template('creater.html')


@app.route('/download/<filename>')
def download(filename):
    return send_from_directory(app.config['INFERENCE_FOLDER'], filename)


@app.route('/upload', methods=['POST'])
def upload():
    try:
        file = request.files['file']
        model_option = request.form['model_option']
        options = {
            '模型1': ('generate.py', ['--emotion', request.form['emotion'], '--is_tempo', request.form['threshold'], '--my_tempo', request.form['tempo'], '--density_threshold', request.form['density_threshold'], '--instrument', request.form['instrument']]),
            '模型2': ('./generate-Demo/gen_midi_conditional.py', [])
        } # 替换成需要评估的模型
        
        if model_option in options:
            script, args = options[model_option]
            filename = file.filename
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)
            args.extend(['--video', file_path])
            subprocess.run(['python', script] + args)
            message = f'视频文件 {filename} 上传成功'
        else:
            message = '无效的模型选项'
            filename = None
    except:
        message = '视频文件上传失败'
        filename = None
    return render_template('creater.html', message=message, filename=filename)




@app.route('/submit', methods=['POST'])
def submit():
    role = request.form.get('role')
    score1_1 = request.form.get('score1_1')
    score1_2 = request.form.get('score1_2')
    score1_3 = request.form.get('score1_3')
    score2_1 = request.form.get('score2_1')
    score2_2 = request.form.get('score2_2')
    score2_3 = request.form.get('score2_3')

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{timestamp}.txt"
    file_path = os.path.join(app.config['TXT_FOLDER'], filename)

    with open(file_path, 'w') as f:
        f.write(f"Role: {role}\n")
        f.write(f"Score1_1: {score1_1}\n")
        f.write(f"Score1_2: {score1_2}\n")
        f.write(f"Score1_3: {score1_3}\n")
        f.write(f"Score2_1: {score2_1}\n")
        f.write(f"Score2_2: {score2_2}\n")
        f.write(f"Score2_3: {score2_3}\n")

    return redirect(url_for('user'))


@app.route('/submit_c', methods=['POST'])
def submit_c():
    role = request.form.get('role')
    modeltmp = request.form.get('modeltmp')
    score1 = request.form.get('score1')
    score2 = request.form.get('score2')
    score3 = request.form.get('score3')
    score4 = request.form.get('score4')
    score5 = request.form.get('score5')
    score6 = request.form.get('score6')

    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"creater_{timestamp}.txt"
    file_path = os.path.join(app.config['CREATER_TXT_FOLDER'], filename)

    with open(file_path, 'w') as f:
        f.write(f"Role: {role}\n")
        f.write(f"modeltmp: {modeltmp}\n")
        f.write(f"Score1: {score1}\n")
        f.write(f"Score2: {score2}\n")
        f.write(f"Score3: {score3}\n")
        f.write(f"Score4: {score4}\n")
        f.write(f"Score5: {score5}\n")
        f.write(f"Score6: {score6}\n")

    return redirect(url_for('creater'))


if __name__ == '__main__':
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['INFERENCE_FOLDER'] = 'inference'
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])
    if not os.path.exists(app.config['INFERENCE_FOLDER']):
        os.makedirs(app.config['INFERENCE_FOLDER'])
    app.config['TXT_FOLDER'] = 'txts'
    if not os.path.exists(app.config['TXT_FOLDER']):
        os.makedirs(app.config['TXT_FOLDER'])
    app.config['CREATER_TXT_FOLDER'] = 'create_txts'
    if not os.path.exists(app.config['CREATER_TXT_FOLDER']):
        os.makedirs(app.config['CREATER_TXT_FOLDER'])
    app.config['VIDEO_FOLDER'] = 'inference_our'
    if not os.path.exists(app.config['VIDEO_FOLDER']):
        os.makedirs(app.config['VIDEO_FOLDER'])

    app.config['CMT_VIDEO_FOLDER'] = 'inference_cmt'
    if not os.path.exists(app.config['CMT_VIDEO_FOLDER']):
        os.makedirs(app.config['CMT_VIDEO_FOLDER'])
    app.run('0.0.0.0',port = 6002, debug=True)
    #app.run()
