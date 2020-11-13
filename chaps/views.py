from django.shortcuts import render, get_object_or_404, redirect
from chaps.models import Chap, Pair, Call, IChap, IPair
from chaps.forms import ChapForm, PairForm, CallForm, SettingsForm
from django.urls import reverse_lazy, reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView, ListView, DetailView,
                                  CreateView, UpdateView, DeleteView)
from django.contrib.auth.models import User
import random, os


def index(request):
  return render(request, 'base.html')


class AboutView(TemplateView):
  template_name = 'chaps/about.html'

# def about(request):
#     act_dir = os.getcwd()
#     data_path = act_dir + "/chaps_project/static/Paar.txt"
#     author = request.user
#
#     n = 0
#     Kapitelalt = "99"
#     IChap.objects.all().delete()
#
#     object_list = Chap.objects.filter(author=author)
#     Chap.objects.filter(author=author).delete()
#
#     with open(data_path, 'r', encoding='utf-8', errors='replace') as datfile:
#       for line in datfile:
#         items_list = line.split(";")
#         if items_list[2] != Kapitelalt:
#           Kapitelalt = items_list[2]
#           Kapitelname = "LF 9-" + items_list[2]
#           Iobj = Chap(author=author, name=Kapitelname)
#           Iobj.save()
#
#         Pobj = Pair.objects.create(
#           chap=Iobj,
#           textL = items_list[3],
#           textR = items_list[4]
#         )
#         Pobj.save()
#         n += 1
#     object_list = Pair.objects.all()
#     return render(request, 'chaps/about.html', {'object_list': object_list})


# @login_required
class ChapListView(ListView):
  template_name = "chaps/chap_list.html"
  model = Chap
  context_object_name = 'chap'

  def get_queryset(self):
    qs = super().get_queryset()
    return qs.filter(author_id=self.request.user.id)


class ChapDetailView(DetailView):
  template_name = "chaps/chap_detail.html"
  model = Chap


class ChapCreateView(LoginRequiredMixin, CreateView):
  form_class = ChapForm
  template_name = "chaps/chap_form.html"
  success_url = reverse_lazy('chaps:chap_list')

  def form_valid(self, form):
    form.instance.author = self.request.user
    return super(ChapCreateView, self).form_valid(form)

  def get_objects(request, pk):
    chap = get_object_or_404(Chap, pk=pk)
    form = ChapForm
    return render(request, 'chaps/chap_form.html', {'form':form, 'object': chap})


class ChapUpdateView(LoginRequiredMixin, UpdateView):
  login_url = '/login/'
  model = Chap
  form_class = ChapForm

  def get_success_url(self):
    return reverse('chaps:chap_list')


class ChapDeleteView(DeleteView):
  model = Chap
  success_url = reverse_lazy('chaps:chap_list')

#____________________________________________________________
# Pair Views

@login_required
def add_pair_to_chap(request, pk):
  objChap= get_object_or_404(Chap, pk=pk)
  form = PairForm()
  context = {
    'form': form,
    'sender': "Create",
    'chap': objChap
  }
  if request.method == 'POST':
    form = PairForm(request.POST)
    if form.is_valid():
      pair = form.save(commit=False)
      pair.chap = objChap
      pair.save()

  return render(request, 'chaps/pair_form.html', context)


@login_required
def pair_update(request, pk, id):
  objPair = get_object_or_404(Pair, id=id)
  objChap = get_object_or_404(Chap, pk=pk)

  # pass the object as instance in form
  form = PairForm(request.POST or None, instance=objPair)

  # save the data from the form and
  # redirect to detail_view
  if form.is_valid():
    form.save()
    return redirect('chaps:chap_detail', pk=objChap.pk)
  else:
    context = {
      'form': form,
      'sender': "Update",
      'chap': objChap
    }
  return render(request, 'chaps/pair_form.html', context)


@login_required
def callPairs(request, pk, ct):

  chap = get_object_or_404(Chap, pk=pk)
  call = Call.objects.first() # for text (given and answered) there is only one object
  # ct calltype (all, called, fail) set via button
  call.callType = ct

  #_________
  if request.method == 'POST':

    form = CallForm(request.POST)
    if form.is_valid():
      cd = form.cleaned_data
      call.textAnswered = cd['textAnswered']
      call.save()
      objPair = chap.pairs.get(id=call.pairAskedID)
      if chap.lr == "L":
        textCalled = objPair.textR
      else:
        textCalled = objPair.textL

      if call.textAnswered == textCalled:
        call.textAnswered = "99"
        objPair.status = 1
        objPair.save()
        chap.sum1 = chap.pairs.filter(status=1).count()
        chap.sum2 = chap.pairs.filter(status=2).count()
        chap.sum1 = chap.sum1 + chap.sum2
        chap.save()
        return redirect('chaps:callPairs', pk=objPair.chap.pk, ct=call.callType)

      context = {'objChap': chap,
                 'objPair': objPair,
                 'ct': call.callType,
                 'lr': chap.lr,
                 'text': call.textAnswered}
      return render(request, 'chaps/check_form.html', context)

  else:
    # ct calltype (all=0, called=1, fail=2) set via button
    # lr: left, right and rs: random, serial set via chap_settings per chap

    pair_list = chap.pairs.all() # ct=0,1,2 alle abfragen

    if ct == 1:  # Rest abfragen
      pair_list = chap.pairs.filter(status=0)

    if ct == 2:  # Fehler abfragen
      pair_list = chap.pairs.filter(status=2)

    # chap.save()

    if pair_list.count() == 0:
      return render(request, 'chaps/chap_detail.html', {'chap': chap})
      # message und Abfrage zurücksetzen

    if chap.rs == "r":
      # erzeuge Zufallzahl zwischen 1 und Anzahl pairs
      if pair_list.count() == 1:
        ir = 1
      else:
        ir = random.randint(1, pair_list.count())

      objPair = pair_list[ir - 1]
      id = objPair.id
    else:
      # serial call
      if ct != 1:
        num = chap.toCallNum0
      else:
        num = 0

      if num > pair_list.count() - 1:
        return render(request, 'chaps/chap_detail.html', {'chap': chap})

      objPair = pair_list[num]
      id = objPair.id

    if chap.lr == "L":
      pair_text = objPair.textL
    else:
      pair_text = objPair.textR

    call.pairAskedID = id
    call.save()

    form = CallForm(request.POST)

    context = {
      'form':form,
      'objChap':chap,
      'pair_text':pair_text,
      'pairs_count': chap.pairs.count(),
      'ct': call.callType
    }
    return render(request, 'chaps/call_form.html', context)


def call_fail(request, pk, id, ct, lr):
  chap = get_object_or_404(Chap, pk=pk)

  objPair = chap.pairs.get(id=id)
  objPair.status = 2
  objPair.save()

  chap.sum1 = chap.pairs.filter(status=1).count() # called OK
  chap.sum2 = chap.pairs.filter(status=2).count() # called fail
  chap.sum1 = chap.sum1 + chap.sum2 # called

  # bei alle abfragen bleibt die pair_list gleich
  # Fehler abfragen: wenn nicht richtig beantwortet bleibt die pair_list gleich
  if ct != 1:
    chap.toCallNum0 += 1

  chap.save()
  return redirect('chaps:callPairs', pk, ct)


def call_OK(request, pk, id, ct, lr):
  chap = get_object_or_404(Chap, pk=pk)

  objPair = chap.pairs.get(id=id)
  objPair.status = 1
  objPair.save()

  chap.sum1 = chap.pairs.filter(status=1).count() # called OK
  chap.sum2 = chap.pairs.filter(status=2).count() # called fail
  chap.sum1 = chap.sum1 + chap.sum2 # called

  # bei alle abfragen bleibt die pair_list gleich
  if ct == 0:
    chap.toCallNum0 += 1

  chap.save()
  return redirect('chaps:callPairs', pk, ct)


def callReset(request, pk):
  chap = get_object_or_404(Chap, pk=pk)
  chap.sum1 = 0
  chap.sum2 = 0
  chap.toCallNum0 = 0
  chap.save()

  for objPair in chap.pairs.all():
    objPair.status = 0
    objPair.save()
  return render(request, 'chaps/chap_detail.html', {'chap': chap})


def settings(request, pk):
  chap = get_object_or_404(Chap, pk=pk)
  if request.method == 'POST':
    chap.lr = request.POST['LR']
    chap.rs = request.POST['rs']
    chap.save()
  else:
    form = SettingsForm()
    context = {}
    context['chap'] = chap
    context['form'] = form
    return render(request, 'chaps/chap_settings.html', context)

  return redirect('chaps:chap_detail', pk=chap.pk)


@login_required
def pair_remove(request, pk, id):
  context = {}
  pair = get_object_or_404(Pair, id=id)
  chap = get_object_or_404(Chap, pk=pk)

  if request.method == "POST":
    pair.delete()
    return redirect('chaps:chap_detail', pk=pk)

  return render(request, 'chaps/pair_confirm_delete.html', {'objChap': chap, 'objPair': pair})





