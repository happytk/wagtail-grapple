import graphene
from ..registry import registry


def SnippetsQuery():
    if registry.snippets:

        class SnippetObjectType(graphene.Union):
            class Meta:
                types = registry.snippets.types

        class Mixin:
            snippets = graphene.List(SnippetObjectType, search_type=graphene.String())
            # Return all snippets.

            def resolve_snippets(self, info, **kwargs):
                snippet_objects = []
                search_type = kwargs.get('search_type')
                for snippet in registry.snippets:
                    if search_type is None or search_type == snippet._meta.model_name:
                        for object in snippet._meta.model.objects.all():
                            snippet_objects.append(object)

                return snippet_objects

        return Mixin

    else:

        class Mixin:
            pass

        return Mixin
