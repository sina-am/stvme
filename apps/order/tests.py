from django.test import TestCase
from apps.order.models import Order
from apps.account.models import User, Translator, SpecializedField, Language
from apps.order import queryset


class TestQuerysets(TestCase):
    def setUp(self):
        l1 = Language.objects.create('persian')
        l2 = Language.objects.create('english')
        f1 = SpecializedField.objects.create('computer')
        
        u = Translator.objects.create(
                user=User.objects.create('sinaaarabi3@gmail.com', 'sina', 'aarabi', 'i1u34b23ibde')
        )
        u.languages.add([l1, l2])
        u.specialized_fields.add(f1)
        
        Translator.objects.bulk_create(translator_list)
        o = Order.objects.create(
            User.objects.create_user('sinaaarabi2@gmail.com', 'sina', 'aarabi', 'i1u34b23ibde'),
            description='test',
            original_text='text',
            deadline=datetime.utcnow(),
            specialized_field=f1,
            type='BOTH',
            source_language=l1,
            target_language=l2
        )
    
    def test_find_best_match(self):
        translators = queryset.find_best_match(o.id)
        self.assertTrue(translator.exists())