export type APIIkeaEntry = {
  pid: string;
  image_url: string;
  name: string;
  price: number;
  explanation: string;
  eco_score: number;
};

export type IkeaEntry = {
  pid: string;
  imageUrl: string;
  name: string;
  price: number;
  explanation: string;
  ecoScore: number;
};

const transformIkeaEntry = (entry: APIIkeaEntry): IkeaEntry => {
  return {
    pid: entry.pid,
    imageUrl: entry.image_url,
    name: entry.name,
    price: entry.price,
    explanation: entry.explanation,
    ecoScore: entry.eco_score,
  };
};

const ikeaEntry1 = {
  pid: "20557875",
  image_url:
    "https://www.ikea.com/se/en/images/products/groensta-chair-with-armrests-in-outdoor-grey-turquoise__1243805_pe920954_s5.jpg?f=xl",
  name: "Chair 1",
  price: 500,
  explanation: "This is a sample explanation of the IKEA product.",
  eco_score: 2,
};

const ikeaEntry2 = {
  pid: "70602069",
  image_url:
    "https://www.ikea.com/se/en/images/products/raevsten-bar-stool-counter-height-black__1447502_pe989132_s5.jpg?f=xl",
  name: "Chair 2",
  price: 1000,
  explanation: "This is a sample explanation of the IKEA product.",
  eco_score: 1,
};

const ikeaEntry3 = {
  pid: "50406465",
  image_url:
    "https://www.ikea.com/se/en/images/products/franklin-bar-stool-with-backrest-foldable-counter-height-black-black__0727485_pe735710_s5.jpg?f=xl",
  name: "Chair 3",
  price: 200,
  explanation: "This is a sample explanation of the IKEA product.",
  eco_score: 0,
};

export class ApiHandler {
  static getIkeaEntryFromUrl(url: string): Promise<IkeaEntry | null> {
    const result: APIIkeaEntry = ikeaEntry1;
    if (result !== null) {
      return Promise.resolve(transformIkeaEntry(result));
    }
    return Promise.resolve(null);
  }

  static getSimilarIkeaEntries(pid: string): Promise<IkeaEntry[]> {
    const entries = [ikeaEntry2, ikeaEntry3];
    const transformedEntries = entries.map(transformIkeaEntry);
    return Promise.resolve(transformedEntries);
  }

  static getItemComparasionExplanation(
    pid1: string,
    pid2: string,
  ): Promise<string> {
    const explanation =
      "This is a sample explanation comparing the two IKEA products.";
    return Promise.resolve(explanation);
  }

  static getMaterialRankingTable(): Promise<
    { material: string; score: number }[]
  > {
    const table = [
      { material: "Wood", score: 5 },
      { material: "Plastic", score: 2 },
      { material: "Metal", score: 4 },
    ];
    return Promise.resolve(table);
  }
}
