/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   rt_malloc.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: pf4 <oui@42.fr>                            +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2024/06/19 14:12:29 by pf4               #+#    #+#             */
/*   Updated: 2024/06/23 13:45:04 by pf4              ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef RT_MALLOC_H
# define RT_MALLOC_H

# include "rt_liberty.h"

typedef struct s_block
{
	struct s_block	*next;
	struct s_block	*prev;
	size_t			size;
	int				level;
}					t_block;

#endif
