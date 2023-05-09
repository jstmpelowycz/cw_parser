from src.modules.parser.parser import Parser

if __name__ == '__main__':
  parser = Parser(path='../data/test1.pdf')
  result = parser.parse()

  print(result)
