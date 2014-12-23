{-# LANGUAGE NoImplicitPrelude #-}

module TypeHole where

data Foo = Foo
data FooFake = FooFake

fooFake :: FooFake
fooFake = FooFake

fooForReal :: Foo
fooForReal = Foo

takesFoo :: Foo -> Foo
takesFoo f = f

