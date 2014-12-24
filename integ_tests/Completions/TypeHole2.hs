{-# LANGUAGE NoImplicitPrelude #-}

module TypeHole where

data Foo = Foo
data Bar = Bar

foo :: Foo
foo = Foo

bar :: Bar
bar = Bar

takes :: Foo -> Bar -> Foo
takes f x = f

