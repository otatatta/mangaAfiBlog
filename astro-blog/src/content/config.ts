import { defineCollection, z } from "astro:content";

const mangaCollection = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    series: z.string(),
    cover_image: z.string().optional().default(""),
    description: z.string(),
    pubDate: z.string(),
    genre: z.string(),
    author_name: z.string(),
    publisher: z.string(),
    expectation_score: z.number().min(1).max(5),
    buzz_level: z.enum(["低", "中", "高"]),
    tags: z.array(z.string()),
    seo_keywords: z.array(z.string()),
    affiliate_url: z.string(),
  }),
});

export const collections = {
  manga: mangaCollection,
};
