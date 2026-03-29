import rss from "@astrojs/rss";
import { getCollection } from "astro:content";
import type { APIContext } from "astro";

export async function GET(context: APIContext) {
  const allManga = await getCollection("manga");
  const sorted = allManga.sort(
    (a, b) => new Date(b.data.pubDate).getTime() - new Date(a.data.pubDate).getTime()
  );

  return rss({
    title: "漫画新刊まとめ",
    description: "今週の新刊漫画をまとめて紹介。期待値・話題性を独自分析。",
    site: context.site!.toString(),
    items: sorted.map((entry) => ({
      title: entry.data.title,
      pubDate: new Date(entry.data.pubDate),
      description: entry.data.description,
      link: `/manga/${entry.slug}/`,
      categories: [entry.data.genre, ...entry.data.tags],
    })),
    customData: `<language>ja</language>`,
  });
}
