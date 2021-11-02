import search
import pipeline
import website_cleaner


def main():
    webpage = search.search()
    raw_data = pipeline.handoff(webpage)
    website_cleaner.container(raw_data)


main()
