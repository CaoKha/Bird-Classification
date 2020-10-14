from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from .models import ImageModel
from .forms import ImageForm
from fastai.vision.all import load_learner, PILImage
from pathlib import Path
import re

base = Path(__file__).resolve().parent.parent
learn = load_learner(base/'classify/models/model.pkl')


def predict_single(img_file):
    '''function to take image and return prediction'''
    pred, pred_idx, probs = learn.predict(PILImage.create(img_file))
    probs_list = [pred, probs[pred_idx].tolist()]
    return probs_list


def index(request):
    form = ImageForm()
    return render(request, 'classify/index.html', {'form': form})


def result(request):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = form.cleaned_data.get("image")
            img_obj = ImageModel.objects.create(name=image.name, image=image)
        # check if image exist on db, delete all replicate
            for img in ImageModel.objects.all().reverse():
                if ImageModel.objects.filter(name=img.name).count() > 1:
                    img.delete()
            my_prediction = predict_single(image)
            plant_class = str(my_prediction[0])
            plant_type = re.search(r'.+?(?=_)', plant_class).group()
            growth_stage = re.search(r'(?<=_)[\w+.-]+', plant_class).group()
            probability = str("{:.3f}".format(float(my_prediction[1])*100))
            content = {
                'plant_type': plant_type,
                'growth_stage': growth_stage,
                'probability': probability,
                'img_obj': img_obj,
            }
    return render(request, 'classify/result.html', content)
