import type { Metadata } from "next";
import Link from "next/link";
import { blogPosts } from "@/lib/data";
import { PageHero } from "@/components/PageHero";
import { Placeholder } from "@/components/Placeholder";
import { IconArrowRight } from "@/components/Icon";

export const metadata: Metadata = { title: "Blog" };

export default function BlogPage() {
  return (
    <>
      <PageHero kicker="Resources" title="Blog" text="Stories from the shop floor to the global stage." />
      <section className="mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8">
        <div className="grid gap-6 lg:grid-cols-3">
          {blogPosts.map((post) => (
            <article key={post.slug} className="flex flex-col overflow-hidden rounded-xl border border-slate-200 bg-white">
              {post.image ? (
                <img
                  src={post.image}
                  alt={post.title}
                  className="aspect-video w-full object-cover"
                />
              ) : (
                <Placeholder
                  label="Blog cover image"
                  ratio="16 / 9"
                  className="w-full"
                />
              )}
              <div className="flex flex-1 flex-col p-5">
                <h2 className="text-lg font-semibold text-brand-900">{post.title}</h2>
                <p className="mt-2 flex-1 text-sm text-slate-600">{post.excerpt}</p>
                <Link
                  href={`/resources/blog/${post.slug}`}
                  className="mt-4 inline-flex items-center gap-1.5 text-sm font-semibold text-brand-700 hover:text-brand-600"
                >
                  Read article
                  <IconArrowRight className="h-3.5 w-3.5" />
                </Link>
              </div>
            </article>
          ))}
        </div>
      </section>
    </>
  );
}
