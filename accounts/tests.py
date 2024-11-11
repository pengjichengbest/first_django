from django.test import TestCase, Client
from django.urls import reverse
from accounts.models import Account, PageLists, PageListFields, PageLayouts, PageLayoutFields
from django.core.files.uploadedfile import SimpleUploadedFile
import csv
import io

class AccountViewsTestCase(TestCase):

    def setUp(self):
        # 初始化测试客户端
        self.client = Client()

        # 创建测试数据
        self.page_list = PageLists.objects.create(name="account_list", label="Account List")
        self.page_layout = PageLayouts.objects.create(name="account_detail", page_list_id=self.page_list)
        self.page_list_field = PageListFields.objects.create(
            page_list_id=self.page_list,
            name="account_name",
            label="Account Name",
            hidden="0",
            type="String",
        )
        self.account = Account.objects.create(
            account_name="Test Account",
            email="test@example.com",
            phone="1234567890",
            address="123 Test Street"
        )

    def test_account_list(self):
        """测试账户列表视图"""
        response = self.client.get(reverse('account_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Account")

    def test_account_detail(self):
        """测试账户详情视图"""
        response = self.client.get(reverse('account_detail', args=[self.account.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Account")

    def test_account_create(self):
        """测试账户创建视图"""
        response = self.client.post(reverse('account_create'), {
            'account_name': 'New Account',
            'email': 'new@example.com',
            'phone': '9876543210',
            'address': '456 New Street'
        })
        self.assertEqual(response.status_code, 302)  # 成功后重定向
        self.assertTrue(Account.objects.filter(account_name="New Account").exists())

    def test_account_edit(self):
        """测试账户编辑视图"""
        response = self.client.post(reverse('account_edit', args=[self.account.id]), {
            'account_name': 'Updated Account',
            'email': 'updated@example.com',
            'phone': '1112223333',
            'address': 'Updated Address'
        })
        self.assertEqual(response.status_code, 302)  # 成功后重定向
        updated_account = Account.objects.get(id=self.account.id)
        self.assertEqual(updated_account.account_name, "Updated Account")

    def test_account_delete(self):
        """测试账户删除视图"""
        response = self.client.post(reverse('account_delete', args=[self.account.id]))
        self.assertEqual(response.status_code, 302)  # 成功后重定向
        self.assertFalse(Account.objects.filter(id=self.account.id).exists())

    def test_export_accounts(self):
        """测试账户导出视图"""
        response = self.client.get(reverse('export_accounts'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/csv')
        content = response.content.decode('utf-8')
        self.assertIn("Test Account", content)

    def test_import_accounts(self):
        """测试账户导入视图"""
        csv_file = io.StringIO()
        writer = csv.writer(csv_file)
        writer.writerow(['account_name', 'email', 'phone', 'address'])
        writer.writerow(['Imported Account', 'imported@example.com', '1112223333', 'Import Street'])
        csv_file.seek(0)

        file = SimpleUploadedFile('accounts.csv', csv_file.read().encode('utf-8'), content_type='text/csv')
        response = self.client.post(reverse('import_accounts'), {'file': file})
        self.assertEqual(response.status_code, 302)  # 成功后重定向
        self.assertTrue(Account.objects.filter(account_name="Imported Account").exists())
