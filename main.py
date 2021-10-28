import search
import pipeline

def main():
    webpage = search.search()
    pipeline.handoff(webpage)


main()
