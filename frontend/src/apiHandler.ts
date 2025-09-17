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

const baseApiUrl = "http://localhost:8091";

export class ApiHandler {
  static async getIkeaEntryFromUrl(url: string): Promise<IkeaEntry | null> {
    const apiUrl = `${baseApiUrl}/entry/`;
    const apiUrlWithQuery = `${apiUrl}?url=${encodeURIComponent(url)}`;
    const request = new Request(apiUrlWithQuery, {
      method: "POST",
      headers: { Accept: "application/json" },
    });

    try {
      const result = await fetch(request);
      if (!result.ok) {
        return null;
      }
      const data: APIIkeaEntry | null = await result.json();
      if (data !== null) {
        return transformIkeaEntry(data);
      }
      return null;
    } catch {
      return null;
    }
  }

  static async getSimilarIkeaEntries(pid: string): Promise<IkeaEntry[]> {
    const apiUrl = `${baseApiUrl}/entry/similar/${pid}`;
    const request = new Request(apiUrl.toString(), {
      method: "GET",
      headers: { Accept: "application/json" },
    });
    await new Promise((resolve) => setTimeout(resolve, 700));
    try {
      const result = await fetch(request);
      if (!result.ok) {
        return [].map(transformIkeaEntry);
      }
      const data: APIIkeaEntry[] = await result.json();
      return data.map(transformIkeaEntry);
    } catch {
      return [].map(transformIkeaEntry);
    }
  }

  static async getItemComparasionExplanation(
    pid1: string,
    pid2: string,
  ): Promise<string | null> {
    const apiUrl = `${baseApiUrl}/entry/compare/`;
    const requestBody = [pid1, pid2];
    const request = new Request(apiUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify(requestBody),
    });

    const result = await fetch(request);
    if (!result.ok) {
      return null;
    }
    const data: string = await result.json();
    return data;
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
