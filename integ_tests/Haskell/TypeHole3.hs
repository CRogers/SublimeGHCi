{-# LANGUAGE NoImplicitPrelude #-}

module TypeHole3 where

data Foo = Foo
data Bar = Bar
data Quux = Quux

takes :: Foo -> Bar -> Quux -> Foo
takes a b c = a

