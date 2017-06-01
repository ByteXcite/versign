from versign import VerSign, Person


def main():
    person = Person(1, "Paul G.", "data/TestSet/Reference/", "data/Processed/")

    versign = VerSign(person)
    versign.plotReferenceFeatureHistograms()
    # versign.train()
    # versign.test("data/TestSet/Questioned/")
    # versign.plotCalculatedDistances("R001")
    # versign.plotCalculatedDistances("R002")
    # versign.plotCalculatedDistances("R003")
    # versign.plotCalculatedDistances("R004")
    # versign.plotCalculatedDistances("R005")


if __name__ == "__main__":
    main()
