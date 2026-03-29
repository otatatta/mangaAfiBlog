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
    stores: z.array(z.object({
      name: z.string(),
      url: z.string(),
      price: z.string().optional(),
    })).optional().default([]),
  }),
});

const salesCollection = defineCollection({
  type: "content",
  schema: z.object({
    title: z.string(),
    store: z.string(),
    description: z.string(),
    sale_type: z.enum(["割引", "ポイント還元", "無料", "クーポン", "キャンペーン"]),
    discount_text: z.string(),
    start_date: z.string(),
    end_date: z.string(),
    sale_url: z.string(),
    target_genres: z.array(z.string()),
    featured_titles: z.array(z.string()).optional().default([]),
    is_active: z.boolean().default(true),
  }),
});

export const collections = {
  manga: mangaCollection,
  sales: salesCollection,
};
