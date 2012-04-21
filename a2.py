def repeat(s, exclaim):
  result = s + s + s
  if exclaim:
    result = result + '!!!'
  return result
    
def main():
  result = repeat('hey', True)
  print result
  
  
if __name__ == '__main__':
  main()
  
  
