import os
from django.shortcuts import render
def handle_error(request):
	return render(request,'404.html')

