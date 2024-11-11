from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib import messages
from django import forms
from django.db import DatabaseError
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.exceptions import ObjectDoesNotExist
from accounts.models import Account, PageLists, PageListFields, PageLayouts, PageLayoutFields
import csv
import logging
from django.http import HttpResponse

# Create your views here.

logger = logging.getLogger(__name__)

def account_list(request):
     try:
          page_list = PageLists.objects.get(name="account_list")
          fields = PageListFields.objects.filter(page_list_id=page_list.id, deleted="0", hidden="0")
          field_data = [{'name': field.name, 'label': field.label} for field in fields]
          field_names = [field.name for field in fields]
          query = request.GET.get("q", "")
          accounts = Account.objects.filter(Q(account_name__icontains=query)).order_by("-created_date") if query else Account.objects.all().order_by("-created_date")
          paginator = Paginator(accounts, 20)
          page_number = request.GET.get('page')
          page_obj = paginator.get_page(page_number)

          return render(request, 'account_list.html', {
               'page_obj': page_obj,
               'field_data': field_data,
               'field_names': field_names,
               'query': query,
          })
     except ObjectDoesNotExist:
          logger.error("页面配置或字段配置未找到", exc_info=True)
          return render(request, 'error.html', {'message': '页面配置未找到，请联系管理员！'})
     except PageNotAnInteger:
          logger.warning("分页参数无效，返回第一页数据")
          page_obj = paginator.get_page(1)
          return render(request, 'account_list.html', {
            'page_obj': page_obj,
            'field_data': field_data,
            'field_names': field_names,
            'query': query,
        })
     except EmptyPage:
          logger.warning("分页超出范围，返回最后一页数据")
          page_obj = paginator.get_page(paginator.num_pages)
          return render(request, 'account_list.html', {
             'page_obj': page_obj,
            'field_data': field_data,
            'field_names': field_names,
            'query': query,
        })
     except Exception as e:
        logger.error("未知错误发生", exc_info=True)
        return render(request, 'error.html', {'message': '加载失败，请稍后重试。'})


def account_detail(request, account_id):
     try:
          account = get_object_or_404(Account, id=account_id)

          page_layout = PageLayouts.objects.get(name="account_detail")
          fields = PageLayoutFields.objects.filter(page_layout_id=page_layout.id, deleted='0')

          
          field_names = [field.name for field in fields]
          field_data = [{'name': field.name, 'label': field.label} for field in fields]
          return render(request, 'account_detail.html', {
               'account': account, 
               'field_names': field_names,
               'field_data': field_data,
          })
     except Http404 as e:
          logger.warning(f"Account with id {account_id} not found: {str(e)}")
          return render(request, 'error.html', {'message': '账户信息未找到，请检查后重试！'})
     except ObjectDoesNotExist as e:
          logger.error(f"Page layout or fields configuration missing: {str(e)}")
          return render(request, 'error.html', {'message': '页面布局或字段配置未找到，请联系管理员！'})
     except Exception as e:
          logger.error(f"Unknown error occurred while processing account detail: {str(e)}", exc_info=True)
          return render(request, 'error.html', {'message': '加载失败，请稍后重试。'})


def account_create(request):
    try:
          if request.method == 'POST':
               form = AccountForm(request.POST)
               if form.is_valid():
                    form.save()
                    return redirect('account_list')
          else:
               form = AccountForm()
          return render(request, 'account_create.html', {'form': form})
    
    except DatabaseError as e:
          logger.error(f"数据库错误：{str(e)}", exc_info=True)
          return render(request, 'error.html', {'message': '保存账户信息失败，请稍后重试！'})
    except Exception as e:
        logger.error(f"未知错误：{str(e)}", exc_info=True)
        return render(request, 'error.html', {'message': '系统错误，请稍后重试！'})
         


def account_edit(request, account_id):
     try:
          account = get_object_or_404(Account, id=account_id)
          if request.method == 'POST':
               form = AccountForm(request.POST, instance=account)
               if form.is_valid():
                    form.save()
                    return redirect('account_list')
          else:
               form = AccountForm(instance=account)
          return render(request, 'account_create.html', {'form': form})
     except DatabaseError as e:
        logger.error(f"数据库错误：无法保存账户信息 - {str(e)}", exc_info=True)
        return render(request, 'error.html', {'message': '保存账户信息失败，请稍后重试！'})

     except Exception as e:
        logger.error(f"未知错误：无法编辑账户 - {str(e)}", exc_info=True)
        return render(request, 'error.html', {'message': '系统错误，请稍后重试！'})


def account_delete(request, account_id):
     try:
          account = get_object_or_404(Account, id=account_id)
          if request.method == "POST":
               account.delete()
               return redirect('account_list')
          return render(request, 'account_conform_delete.html', {'account': account})
     except DatabaseError as e:
        logger.error(f"数据库错误：无法删除账户 - {str(e)}", exc_info=True)
        return render(request, 'error.html', {'message': '删除账户失败，请稍后重试！'})

     except Exception as e:
        logger.error(f"未知错误：无法删除账户 - {str(e)}", exc_info=True)
        return render(request, 'error.html', {'message': '系统错误，请稍后重试！'})


def export_accounts(request):
     try:
          response = HttpResponse(content_type='text/csv')
          response['Content-Disposition'] = 'attachment; filename="accounts.csv"'
          writer = csv.writer(response)
          writer.writerow(['Account Name', 'Email', 'Phone', 'Address'])
          query = request.GET.get("q", "")
          accounts = Account.objects.filter(Q(account_name__icontains=query)).order_by("-created_date") if query else Account.objects.all().order_by("-created_date")
          for account in accounts:
               writer.writerow([account.account_name, account.email, account.phone, account.address])
          return response
     except DatabaseError as e:
        logger.error(f"数据库错误：无法导出账户数据 - {str(e)}", exc_info=True)
        return HttpResponse("导出失败：数据库错误，请稍后重试！", status=500)

     except Exception as e:
        logger.error(f"未知错误：无法导出账户数据 - {str(e)}", exc_info=True)
        return HttpResponse("导出失败：系统错误，请稍后重试！", status=500)

def import_accounts(request):
     try:
          if request.method == "POST":
               form = ImportFileForm(request.POST, request.FILES)
               if form.is_valid():
                    file = form.cleaned_data['file']
                    decoded_file = file.read().decode('utf-8').splitlines()
                    reader = csv.reader(decoded_file)
                    header = next(reader)

                    FIELD_MAPPING = {
                         'account_name': 0,
                         'email': 1,
                         'phone': 2,
                         'address': 3,
                    }

                    row_number = 1
                    accounts_to_create = [] 

                    for row in reader:
                         row_number += 1

                         data = {key: (row[index].strip() if len(row) > index else None) for key, index in FIELD_MAPPING.items()}
                         
                         # 验证用户名不能为空
                         if not data['account_name']:
                              messages.error(request, f"Error: Account name is empty in row {row_number}. Import stopped.")
                              return render(request, 'import_accounts.html', {'form': form})

                         accounts_to_create.append(
                              Account(
                              account_name=data['account_name'],
                              email=data['email'],
                              phone=data['phone'],
                              address=data['address']
                              )
                         )

                    # 批量创建对象
                    Account.objects.bulk_create(accounts_to_create)
                    messages.success(request, f"Successfully imported {len(accounts_to_create)} accounts.")
                    return redirect('account_list')
          else:
               form = ImportFileForm()

          return render(request, 'import_accounts.html', {'form': form})
     except DatabaseError as e:
        logger.error(f"数据库错误：无法导入账户数据 - {str(e)}", exc_info=True)
        messages.error(request, "导入失败：数据库错误，请稍后重试！")
        return redirect('import_accounts')

     except csv.Error as e:
        logger.error(f"CSV 文件处理错误：{str(e)}", exc_info=True)
        messages.error(request, "导入失败：CSV 文件格式错误，请检查文件内容！")
        return redirect('import_accounts')

     except Exception as e:
        logger.error(f"未知错误：无法导入账户数据 - {str(e)}", exc_info=True)
        messages.error(request, "导入失败：系统错误，请稍后重试！")
        return redirect('import_accounts')



class AccountForm(forms.ModelForm):
     class Meta:
          model = Account
          fields = ['account_name', 'email', 'phone', 'address']


class ImportFileForm(forms.Form):
    file = forms.FileField(label='Select a CSV file')

