import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { findBlogPost } from "@/lib/data";
import { PageHero } from "@/components/PageHero";
import { Placeholder } from "@/components/Placeholder";
import { IconArrowRight } from "@/components/Icon";
import Link from "next/link";

type Props = { params: Promise<{ slug: string }> };

export async function generateStaticParams() {
  const { blogPosts } = await import("@/lib/data");
  return blogPosts.map((post) => ({ slug: post.slug }));
}

export async function generateMetadata({ params }: Props): Promise<Metadata> {
  const { slug } = await params;
  const post = findBlogPost(slug);
  if (!post) return { title: "Blog" };
  return { title: post.title };
}

export default async function BlogDetailPage({ params }: Props) {
  const { slug } = await params;
  const post = findBlogPost(slug);

  if (!post) notFound();

  return (
    <>
      <PageHero kicker="Resources" title={post.title} />
      <article className="mx-auto max-w-4xl px-4 py-16 sm:px-6 lg:px-8">
        {post.image ? (
          <img
            src={post.image}
            alt={post.title}
            className="aspect-video w-full rounded-xl object-cover"
          />
        ) : (
          <Placeholder
            label={`${post.title} cover image`}
            ratio="16 / 9"
            className="mb-8 rounded-xl"
          />
        )}
        <div className="prose prose-slate max-w-none text-sm leading-7">
          {post.content.map((paragraph, idx) => (
            <p key={idx}>{paragraph}</p>
          ))}
        </div>
        <Link
          href="/resources/blog"
          className="mt-8 inline-flex items-center gap-1.5 text-sm font-semibold text-brand-700 hover:text-brand-600"
        >
          Back to all articles
          <IconArrowRight className="h-3.5 w-3.5" />
        </Link>
      </article>
    </>
  );
}
