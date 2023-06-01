
import csv
def open_file(filename):
        file = open("C:\\Users\\LENOVO\\PycharmProjects\\web_scraping\\" + filename + '.csv', 'w', newline="");
        writer = csv.writer(file)
        yield writer
        yield file
def closefile(file):
    file.close()
