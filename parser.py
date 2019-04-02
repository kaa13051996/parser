from os import listdir
from os.path import join, basename
from re import sub
from statistics import mean


class Parser:
    def __init__(self, file_name):
        self.name, self.data = self.read_file(file_name)
        self.__count_records = 10
        self.__records = self.split_list(self.data, self.__count_records)
        self.__features, self.__train, self.__test = self.get_structure()
        self.mean_ones = [row.count('1') / len(row) for row in self.__features]
        self.mean_train = [mean(row) for row in self.__train]
        self.mean_test = [mean(row) for row in self.__test]

    @staticmethod
    def read_file(file_name):
        f = open(file_name, 'r', encoding='utf-8')
        data = f.readlines()
        name = f.name
        f.close()
        return name, data

    @staticmethod
    def split_list(data, count_path=10):
        k, m = divmod(len(data), count_path)
        return [data[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(count_path)]

    def get_structure(self):
        '''
        Конвертирует: string (123,123) -> float (123.123). Уберает подстроки: ' ', '\n', 'Обуч: ', 'Тест: '.
        Структура:
        0 - признаки;
        1,3 - обучение;
        2,4 - тестирование.
        :return: признаки [__count_records], обучение [__count_records*2], тестирование [__count_records*2].

        '''
        features = [sub(r'[ \n]', '', row) for row in [record[0] for record in self.__records]]
        train = self.split_list([float(elem.replace(',', '.')) for elem in [sub(r'[Обуч: \n]', '', row) for row in
                                                                            [record[i] for record in self.__records for
                                                                             i in [1, 3]]]], self.__count_records)
        test = self.split_list([float(elem.replace(',', '.')) for elem in [sub(r'[Тест: \n]', '', row) for row in
                                                                           [record[i] for record in self.__records for i
                                                                            in [2, 4]]]], self.__count_records)
        return features, train, test

    def write_file(self):
        sep = ';'
        data = [basename(self.name), self.mean_ones, self.mean_train, self.mean_test]
        with open('statistics.csv', 'a') as file:
            for item in data:
                file.write(str(item) + sep)
            file.write('\n')


if __name__ == '__main__':
    DIR_DATA = r'data\SSO+SSD'
    list_files = listdir(DIR_DATA)
    full_files = [join(DIR_DATA, file_name) for file_name in list_files]
    obj = Parser(full_files[0])
    obj.write_file()
    print('Win!!!')
