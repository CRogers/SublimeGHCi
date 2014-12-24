{-# LANGUAGE NoImplicitPrelude #-}

module TypeHole2 where

data Foo = Foo
data Bar = Bar

takes :: Foo -> Bar -> Foo
takes a b = a

