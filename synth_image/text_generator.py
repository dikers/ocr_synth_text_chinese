class TextGenerator:
    def __init__(self, text_file):

        with open(text_file, 'r', encoding='utf-8') as f:
            self.lines = f.readlines()
        self.line_index = 0
        self.line_total = len(self.lines)
        print("-" * 30)
        print("line total count: {} ".format(self.line_total))
        print("-" * 30)

    def _next_string(self):
        temp = self.lines[self.line_index].replace("\n", '')
        self.line_index += 1

        if (self.line_index >= self.line_total):
            self.line_index = 0
        return temp

    def _next_batch(self, num):

        text_list = []
        for i in range(0, num):
            text_list.append(self._next_string())

        return '#_#'.join(text_list)


    def create_text_list(self, page_count, line_count):

        page_list = []
        for i in range(page_count):
            page_list.append(self._next_batch(line_count))

        return page_list

if __name__ == "__main__":

    text_generator = TextGenerator('../dataset/text_split.txt')

    print(text_generator.create_text_list(2, 5))

