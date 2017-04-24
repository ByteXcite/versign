from versign import Person, train

if __name__ == "__main__":
    person1 = Person(1, "Tanya")
    train(person1, "data/TrainingSet/Reference/", "data/Processed/")

    person2 = Person(2, "Paul G.")
    train(person2, "data/TestSet/Reference/", "data/Processed/")
