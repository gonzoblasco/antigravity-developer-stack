import { Suspense } from 'react';

interface Props {
  params: { id: string };
  searchParams: { [key: string]: string | string[] | undefined };
}

export default async function Page({ params, searchParams }: Props) {
  // 1. Fetch data directly in component
  // const data = await getData(params.id);

  return (
    <section className="flex flex-col gap-4">
      <header>
        <h1 className="text-2xl font-bold">Page Title</h1>
      </header>

      <Suspense fallback={<div>Loading...</div>}>
        {/* <AsyncComponent /> */}
        <div className="p-4 border rounded">
          Content goes here
        </div>
      </Suspense>
    </section>
  );
}
