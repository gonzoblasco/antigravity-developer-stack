import { expectTypeOf, test } from 'vitest'

// Example Type to Test
interface Avatar {
  size: 'sm' | 'md' | 'lg'
  url: string
}

test('Avatar props are correctly typed', () => {
  // Test property existence
  expectTypeOf<Avatar>().toHaveProperty('size')
  
  // Test property type match
  expectTypeOf<Avatar['size']>().toEqualTypeOf<'sm' | 'md' | 'lg'>()
  
  // Test invalid types serve as negation test
  expectTypeOf<Avatar['size']>().not.toBeString()
})
