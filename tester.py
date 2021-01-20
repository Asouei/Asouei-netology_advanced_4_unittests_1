from main import *
from unittest import TestCase
from unittest.mock import patch

def mock_secretary_program_start(command):
        while True:
            user_command = command
            if user_command == 'p':
                owner_name = get_doc_owner_name()
                print('Владелец документа - {}'.format(owner_name))
            elif user_command == 'ap':
                uniq_users = get_all_doc_owners_names()
                print('Список владельцев документов - {}'.format(uniq_users))
            elif user_command == 'l':
                show_all_docs_info()
            elif user_command == 's':
                directory_number = get_doc_shelf()
                print('Документ находится на полке номер {}'.format(directory_number))
            elif user_command == 'a':
                print('Добавление нового документа:')
                new_doc_shelf_number = add_new_doc()
                print('\nНа полку "{}" добавлен новый документ:'.format(new_doc_shelf_number))
            elif user_command == 'd':
                doc_number, deleted = delete_doc()
                if deleted:
                    print('Документ с номером "{}" был успешно удален'.format(doc_number))
            elif user_command == 'm':
                move_doc_to_shelf()
            elif user_command == 'as':
                shelf_number, added = add_new_shelf()
                if added:
                    print('Добавлена полка "{}"'.format(shelf_number))
            elif user_command == 'help':
                print(secretary_program_start.__doc__)
            elif user_command == 'q':
                break
            else:
                return "No such command"

def mock_get_all_doc_owners_names():
    users_list = []
    for current_document in documents:
        try:
            doc_owner_name = current_document['name']
            users_list.append(doc_owner_name)
        except KeyError:
            pass
    return 'Passed'

def mock_get_doc_owner_name(number):
    user_doc_number = number
    print()
    doc_exist = check_document_existance(user_doc_number)
    if doc_exist:
        for current_document in documents:
            doc_number = current_document['number']
            if doc_number == user_doc_number:
                return True

def mock_remove_doc_from_shelf(doc_number):
    test = False
    for directory_number, directory_docs_list in directories.items():
        if doc_number in directory_docs_list:
            directory_docs_list.remove(doc_number)
            test = True
            break

    return test

def mock_add_new_shelf(shelf_number):
    if shelf_number not in directories.keys():
        directories[shelf_number] = []
        return True
    return False

def mock_delete_doc(number):
    user_doc_number = number
    doc_exist = check_document_existance(user_doc_number)
    if doc_exist:
        for current_document in documents:
            doc_number = current_document['number']
            if doc_number == user_doc_number:
                documents.remove(current_document)
                remove_doc_from_shelf(doc_number)
                return True

def mock_get_doc_shelf(number):
    user_doc_number = number
    doc_exist = check_document_existance(user_doc_number)
    if doc_exist:
        for directory_number, directory_docs_list in directories.items():
            if user_doc_number in directory_docs_list:
                return True
    else:
        return False

def mock_move_doc_to_shelf(a, b):
    user_doc_number = a
    user_shelf_number = b
    remove_doc_from_shelf(user_doc_number)
    append_doc_to_shelf(user_doc_number, user_shelf_number)
    print('Документ номер "{}" был перемещен на полку номер "{}"'.format(user_doc_number, user_shelf_number))
    return True

def mock_add_new_doc(a, b, c, d):
    new_doc_number = a
    new_doc_type = b
    new_doc_owner_name = c
    new_doc_shelf_number = d
    new_doc = {
        "type": new_doc_type,
        "number": new_doc_number,
        "name": new_doc_owner_name
    }
    documents.append(new_doc)
    append_doc_to_shelf(new_doc_number, new_doc_shelf_number)
    print(new_doc_shelf_number)
    return True


class TestSecretary(TestCase):

    @patch('main.secretary_program_start', side_effect = mock_secretary_program_start)
    def test_wrong_command(self, secretary_program_start):
        self.assertEqual(secretary_program_start('asda'), "No such command")

    @patch('main.get_all_doc_owners_names', side_effect = mock_get_all_doc_owners_names)
    def test_get_all_doc_owners_names(self, get_all_doc_owners_names):
        self.assertEqual(get_all_doc_owners_names(), "Passed")

    def test_check_document_existance_normal(self):
        self.assertEqual(check_document_existance('11-2'), True)

    def test_check_document_existance_bad(self):
        self.assertEqual(check_document_existance('11-22'), False)

    def test_check_document_existance_empty(self):
        self.assertEqual(check_document_existance(''), False)

    @patch('main.get_doc_owner_name', side_effect=mock_get_doc_owner_name)
    def test_get_doc_owner_name_exist_none(self, get_doc_owner_name):
        self.assertEqual(get_doc_owner_name('11-22'), None)


    @patch('main.get_doc_owner_name', side_effect=mock_get_doc_owner_name)
    def test_get_doc_owner_name_not_exist(self, get_doc_owner_name):
        self.assertEqual(get_doc_owner_name('11-22'), None)

    @patch('main.remove_doc_from_shelf', side_effect=mock_remove_doc_from_shelf)
    def test_remove_doc_from_shelf(self, remove_doc_from_shelf):
        self.assertEqual(remove_doc_from_shelf('11-2'), True)

    @patch('main.remove_doc_from_shelf', side_effect=mock_remove_doc_from_shelf)
    def test_remove_doc_from_shelf(self, remove_doc_from_shelf):
        self.assertEqual(remove_doc_from_shelf('11-22'), False)

    @patch('main.add_new_shelf', side_effect=mock_add_new_shelf)
    def test_add_new_shel_exist(self, add_new_shelf):
        self.assertEqual(add_new_shelf('1'), False)

    @patch('main.add_new_shelf', side_effect=mock_add_new_shelf)
    def test_add_new_shel_exist(self, add_new_shelf):
        self.assertEqual(add_new_shelf('123'), True)

    def test_append_doc_to_shelf(self):
        self.assertEqual(append_doc_to_shelf('3123', '1'), True)

    @patch('main.delete_doc', side_effect=mock_delete_doc)
    def test_delete_doc_exist(self, delete_doc):
        self.assertEqual(delete_doc('11-2'), True)

    @patch('main.delete_doc', side_effect=mock_delete_doc)
    def test_delete_doc_not_exist(self, delete_doc):
        self.assertEqual(delete_doc('11-22'), None)

    @patch('main.get_doc_shelf', side_effect=mock_get_doc_shelf)
    def test_get_doc_shelf_exist(self, get_doc_shelf):
        self.assertEqual(get_doc_shelf('11-2'), True)

    @patch('main.get_doc_shelf', side_effect=mock_get_doc_shelf)
    def test_get_doc_shelf_exist(self, get_doc_shelf):
        self.assertEqual(get_doc_shelf('11-22'), False)

    @patch('main.move_doc_to_shelf', side_effect=mock_move_doc_to_shelf)
    def test_move_doc_to_shelf_working(self, move_doc_to_shelf):
        self.assertEqual(move_doc_to_shelf('11-2', '3'), True)

    def test_show_all_docs_info(self):
        self.assertEqual(show_all_docs_info(), True)

    @patch('main.add_new_doc', side_effect=mock_add_new_doc)
    def test_add_new_doc_working(self, add_new_doc):
        self.assertEqual(add_new_doc('12', 'Passport', 'Alex Alexov', '1'), True)