from versign import VerSign, Person


def main():
    person = Person(1, "Paul G.", "data/TestSet/Reference/", "data/Processed/")

    versign = VerSign(person)
    # versign.train()
    versign.test("data/TestSet/Questioned/")

if __name__ == "__main__":
    main()
