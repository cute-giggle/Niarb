from django.shortcuts import render
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.http import HttpResponse

import os
import pandas as pd
import json
import shutil
import sys
import glob

from .models import UserNote

from .data import indicator_guide
from .data import FsaverageMesh, FsaverageAnnot


WORKING_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../data/working')
BENCHMARK_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../../../data/benchmark')


def index(request):
    return render(request, 'index.html')


def get_subj_dir(subj_id: str, category: str):
    subj_dir = os.path.join(WORKING_DIR, category, 'subjects', subj_id)
    return subj_dir


def load_benchmark(category: str, file_name: str):
    benchmark_path = os.path.join(BENCHMARK_DIR, category, file_name)
    if file_name.split('.')[-1] == 'csv':
        benchmark = pd.read_csv(benchmark_path)
        benchmark = json.loads(benchmark.reset_index().to_json(orient='records'))

    elif file_name.split('.')[-1] == 'json':
        benchmark = []
        with open(benchmark_path, 'r') as f:
            data = json.load(f)
        index = 0
        for key, value in data.items():
            if 'distribution' in value:
                value['index'] = index
                value['indicator_name'] = key
                benchmark.append(value)
                index += 1
            elif isinstance(value, dict):
                for k, v in value.items():
                    v['index'] = index
                    v['indicator_name'] = key + ' ' + k
                    benchmark.append(v)
                    index += 1
    
    return benchmark


def structural(request):
    # 加载基准数据
    benchmark = load_benchmark('smri', 'benchmark.csv')

    # 根据用户名查询用户的所有记录
    username = request.user.username
    user_records = UserNote.objects.filter(username=username, category='smri').values('id', 'category', 'status', 'create_time', 'update_time')

    for user_record in user_records:

        # 如果记录的状态为processing，检查是否已经完成处理，如果已经完成，更新记录状态为processed，否则更新记录状态为failed
        if user_record['status'] == 'processing':
            subj_dir = get_subj_dir(user_record['id'], user_record['category'])
            if os.path.exists(os.path.join(subj_dir, 'completed.txt')):
                if os.path.exists(os.path.join(subj_dir, 'report_result/report.csv')):
                    user_record['status'] = 'processed'
                else:
                    user_record['status'] = 'failed'
                UserNote.objects.filter(id=user_record['id']).update(status=user_record['status'])

    return render(request, 'structural.html', locals())


def functional(request):
    # 加载基准数据
    benchmark = load_benchmark('fmri', 'benchmark.json')

    # 根据用户名查询用户的所有记录
    username = request.user.username
    user_records = UserNote.objects.filter(username=username, category='fmri').values('id', 'category', 'status', 'create_time', 'update_time')

    for user_record in user_records:

        # 如果记录的状态为processing，检查是否已经完成处理，如果已经完成，更新记录状态为processed，否则更新记录状态为failed
        if user_record['status'] == 'processing':
            subj_dir = get_subj_dir(user_record['id'], user_record['category'])
            if os.path.exists(os.path.join(subj_dir, 'completed.txt')):
                if os.path.exists(os.path.join(subj_dir, 'report_result/report.csv')):
                    user_record['status'] = 'processed'
                else:
                    user_record['status'] = 'failed'
                UserNote.objects.filter(id=user_record['id']).update(status=user_record['status'])

    return render(request, 'functional.html', locals())


def diffusion(request):
    # 加载基准数据
    benchmark = load_benchmark('dmri', 'benchmark.json')

    # 根据用户名查询用户的所有记录
    username = request.user.username
    user_records = UserNote.objects.filter(username=username, category='dmri').values('id', 'category', 'status', 'create_time', 'update_time')

    for user_record in user_records:

        # 如果记录的状态为processing，检查是否已经完成处理，如果已经完成，更新记录状态为processed，否则更新记录状态为failed
        if user_record['status'] == 'processing':
            subj_dir = get_subj_dir(user_record['id'], user_record['category'])
            if os.path.exists(os.path.join(subj_dir, 'completed.txt')):
                if os.path.exists(os.path.join(subj_dir, 'report_result/report.csv')):
                    user_record['status'] = 'processed'
                else:
                    user_record['status'] = 'failed'
                UserNote.objects.filter(id=user_record['id']).update(status=user_record['status'])

    return render(request, 'diffusion.html', locals())


def surface(request):
    return render(request, 'surface.html')


def login(request):
    if request.method == 'POST':
        print(request.path)
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/index/')
        else:
            return render(request, 'login.html')
    else:
        return render(request, 'login.html')


@login_required
def logout(request):
    auth.logout(request)
    return redirect('/index/')


def signup(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = User.objects.create_user(username=username, email=email, password=password)
        except Exception as e:
            print(e)
            return render(request, 'signup.html')
        
        user.save()
        return redirect('/login/')
    else:
        print(request)
        return render(request, 'signup.html')


def file_intact_check(subj_id: str, category: str):
    file_dir = get_subj_dir(subj_id, category)
    file_list = os.listdir(file_dir)
    
    if category == 'smri':
        return len(file_list) == 1
    elif category == 'fmri':
        return len(file_list) >= 2
    else:
        return len(file_list) >= 3


def file_save(file, category: str, username: str, subj_id: str):

    file_dir = get_subj_dir(subj_id, category)

    if not os.path.exists(file_dir):
        os.makedirs(file_dir, exist_ok=True)

    file_path = os.path.join(file_dir, file.name)
    
    with open(file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)

    if UserNote.objects.filter(id=subj_id).exists():
        return

    if file_intact_check(subj_id, category):
        user_record = UserNote.objects.create(id=subj_id, username=username, category=category, status='unprocessed')
        user_record.save()


@login_required
def file_accept(request):
    if request.method == 'POST':
        files = request.FILES.get('upload_file')
        if files is None:
            return HttpResponse(json.dumps({'fileuploaded': 'failed'}))

        username = request.user.username
        subj_id = request.POST.get('subj_id')
        catagory = request.POST.get('category')
        file_save(request.FILES.get('upload_file'), catagory, username, subj_id)

        return HttpResponse(json.dumps({'fileuploaded': 'success'}))


def process_user_record(request):
    id = request.POST.get('id')
    user_record = UserNote.objects.get(id=id)
    if user_record is None or user_record.status != 'unprocessed':
        return

    user_record.status = 'processing'
    user_record.save()

    script_path = os.path.join(os.path.dirname(__file__), 'image_interface.py')
    log_path = os.path.join(get_subj_dir(user_record.id, user_record.category), 'log.txt')
    os.system('nohup python {} --subj_id {} --category {} >{} 2>&1 &'.format(script_path, user_record.id, user_record.category, log_path))

    return HttpResponse(json.dumps({'process': 'success'}))


def delete_user_record(request):
    id = request.POST.get('id')
    user_record = UserNote.objects.get(id=id)
    if user_record:
        category = user_record.category
        data_dir = get_subj_dir(user_record.id, category)
        if os.path.exists(data_dir):
            shutil.rmtree(data_dir)
        user_record.delete()

    return HttpResponse(json.dumps({'delete': 'success'}))


def get_user_report(request):
    id = request.POST.get('id')
    user_record = UserNote.objects.get(id=id)
    if user_record is None or user_record.status != 'processed':
        return

    report_path = os.path.join(get_subj_dir(user_record.id, user_record.category), 'report_result/report.csv')
    report = pd.read_csv(report_path)
    abnormal = report[report['conclusion'] != 'normal']
    report = json.loads(report.reset_index().to_json(orient='records'))
    abnormal = json.loads(abnormal.reset_index().to_json(orient='records'))
    for i in range(len(abnormal)):
        indicator_name = abnormal[i]['indicator_name']
        conclusion = abnormal[i]['conclusion']
        category = user_record.category
        abnormal[i]['guide'] = indicator_guide.get_indicator_guide(category, indicator_name, conclusion)

    img_dir = os.path.join(get_subj_dir(user_record.id, user_record.category), 'report_result')
    img_list = [os.path.basename(img) for img in glob.glob(os.path.join(img_dir, '*.png'))]
    img_list = ['/static/subjects/' + user_record.id + '/report_result/' + img for img in img_list]

    return HttpResponse(json.dumps({'report': report, 'abnormal': abnormal, 'img_list': img_list}))


def askme(request):
    if request.method == 'POST':
        question = request.POST.get('question')
        
        from .image_interface import prepare_env
        prepare_env()
        from chatgpt.chatgpt_caller import ChatGPTCaller
        caller = ChatGPTCaller()
        try:
            answer = caller.call_simple(question)['choices'][0]['message']['content']
        except Exception as e:
            print(e)
            answer = 'Sorry, I cannot answer your question.'
        
    return HttpResponse(json.dumps({'answer': answer}))


def get_fsaverage_mesh(request):
    if request.method != 'GET':
        return HttpResponse(json.dumps({'error': 'method not allowed'}))
    mesh_name = request.GET.get('mesh_name') + '.mesh'
    data = FsaverageMesh(mesh_name).get_data()
    return HttpResponse(json.dumps(data))


def get_fsaverage_annot(request):
    if request.method != 'GET':
        return HttpResponse(json.dumps({'error': 'method not allowed'}))
    annot_name = request.GET.get('annot_name') + '.annot'
    data = FsaverageAnnot(annot_name).get_data()
    return HttpResponse(json.dumps(data))
